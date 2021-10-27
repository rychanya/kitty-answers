<template>
  <template v-if="type === 'Выберите один правильный вариант'">
    <div v-for="el in answers" :key="el">
      <div class="columns is-gapless is-mobile is-vcentered">
        <div class="column is-narrow">
          <span v-if="el === answer" class="icon has-text-success">
            <i class="fas fa-check"></i>
          </span>
          <span v-else class="icon has-text-danger">
            <i class="fas fa-ban"></i>
          </span>
        </div>
        <div class="column">
          {{ el }}
        </div>
      </div>
    </div>
  </template>

  <template v-else-if="type === 'Выберите все правильные варианты'">
    <div v-for="el in answers" :key="el">
      <div class="columns is-gapless is-mobile is-vcentered">
        <div class="column is-narrow">
          <span v-if="answer.includes(el)" class="icon has-text-success">
            <i class="fas fa-check"></i>
          </span>
          <span v-else class="icon has-text-danger">
            <i class="fas fa-ban"></i>
          </span>
        </div>
        <div class="column">
          {{ el }}
        </div>
      </div>
    </div>
  </template>

  <template
    v-else-if="
      type ===
      'Перетащите варианты так, чтобы они оказались в правильном порядке'
    "
  >
    <div v-for="(el, index) in answers" :key="el">
      <div class="columns is-gapless is-mobile is-vcentered">
        <div class="column is-narrow mr-1">
          <strong>{{ index + 1 }} </strong>
        </div>
        <div class="column">
          {{ el }}
        </div>
      </div>
    </div>
  </template>

  <template
    v-else-if="
      type === 'Соедините соответствия справа с правильными вариантами'
    "
  >
    <div v-for="(el1, el2) in answer" :key="el1">
      <div class="columns is-gapless is-mobile is-vcentered">
        <div class="column">{{ el1 }}</div>
        <div class="column is-narrow mr-1 ml-1">-</div>
        <div class="column">{{ el2 }}</div>
      </div>
    </div>
  </template>
</template>

<script lang="ts">
interface StrDictionary {
  [index: string]: string;
}
type answerType = string | Array<string> | StrDictionary;

import { defineComponent, PropType } from "vue";

export default defineComponent({
  props: {
    answer: Object as PropType<answerType>,
    answers: Object as PropType<Array<string>>,
    type: String,
  },
});
</script>

<style></style>
