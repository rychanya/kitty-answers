<template>
  <div class="container">
    <div class="content">
      <h1>Поддержите существование котят</h1>
      <p>Пожертвованные средства пойдут на аренду платного сервера.</p>
    </div>
    <div class="content">
      <iframe
        class="has-ratio"
        :src="srcURL"
        width="100%"
        height="222"
        frameborder="0"
        scrolling="no"
      ></iframe>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "Home",
  setup() {
    const srcURL =
      "https://yoomoney.ru/quickpay/shop-widget?writer=seller&targets=%D0%9D%D0%B0%20%D0%BA%D0%BE%D1%82%D1%8F%D1%82&targets-hint=&default-sum=100&button-text=14&payment-type-choice=on&hint=&successURL=&quickpay=shop&account=4100117309756050&";
    return { srcURL };
  },
});
</script>
