<template>
  <QA v-if="qa" :full="true" :qa="qa"></QA>
</template>

<script lang="ts">
import { defineComponent, watch, ref } from "vue";
import { useRoute } from "vue-router";
import QA from "@/components/QA.vue";
import { QA as QAModel } from "@/api/models";
import { get } from "@/api/search";

export default defineComponent({
  components: { QA },

  setup() {
    let router = useRoute();
    let id = ref(router.params.id);
    let qa = ref<QAModel>();
    function fetchData() {
      get(id.value).then((data) => (qa.value = data));
    }
    fetchData();
    return { id, qa };
  },
});
</script>

<style></style>
