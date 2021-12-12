from hypothesis import strategies

from adapters.QAStorage.AbstractQAStorage import QADTO, GroupDTO, QuestionDTO
from answers.models.qa import QATypeEnum

valid_text = (
    strategies.text(min_size=1, max_size=200)
    .map(lambda s: s.strip())
    .filter(lambda s: len(s) > 0)
)


@strategies.composite
def QuestionDTOSrtategies(
    draw: strategies.DrawFn, type: QATypeEnum = None, question: str = None
) -> QuestionDTO:
    if question is None:
        question = draw(valid_text)
    if type is None:
        type = draw(strategies.sampled_from(QATypeEnum))
    return QuestionDTO(question=question, type=type)


@strategies.composite
def GroupDTOSrtategies(draw: strategies.DrawFn, type: QATypeEnum = None) -> GroupDTO:
    if type is None:
        type = draw(strategies.sampled_from(QATypeEnum))
    answers = draw(
        strategies.lists(
            valid_text,
            min_size=2,
            max_size=6,
            unique=True,
        )
    )
    if type == QATypeEnum.MatchingChoice:
        extra_answers = draw(
            strategies.lists(
                valid_text, min_size=len(answers), max_size=len(answers), unique=True
            )
        )
    else:
        extra_answers = []
    return GroupDTO(all_answers=answers, all_extra_answers=extra_answers)


@strategies.composite
def QADTOSrtategies(
    draw: strategies.DrawFn, type: QATypeEnum = None, question: str = None
) -> QADTO:
    _question = draw(QuestionDTOSrtategies(type=type, question=question))
    _group = draw(GroupDTOSrtategies(type=_question.type) | strategies.none())
    _is_correct = draw(strategies.booleans())
    all_answers = (
        _group.all_answers
        if _group
        else draw(
            strategies.lists(
                valid_text,
                min_size=2,
                max_size=6,
                unique=True,
            )
        )
    )
    if _question.type == QATypeEnum.OnlyChoice:
        _answer = [draw(strategies.sampled_from(all_answers))]
    elif _question.type == QATypeEnum.MultipleChoice:
        _answer = draw(
            strategies.lists(
                strategies.sampled_from(all_answers),
                unique=True,
                min_size=1,
                max_size=len(all_answers),
            )
        )
    else:
        _answer = draw(
            strategies.lists(
                strategies.sampled_from(all_answers),
                unique=True,
                min_size=len(all_answers),
                max_size=len(all_answers),
            )
        )

    return QADTO(
        question=_question.dict(),
        group=(_group.dict() if _group else None),
        is_correct=_is_correct,
        answer=_answer,
    )
