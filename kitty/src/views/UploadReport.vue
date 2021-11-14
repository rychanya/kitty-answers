<template>
  <div class="container">{{ upload }}{{ id }}</div>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from "vue";
import { useRoute } from "vue-router";
import { get_upload } from "@/api/search";

export default defineComponent({
  setup() {
    let router = useRoute();
    let id = computed(() => {
        return router.params.id
    })
    let upload = ref();
    // function fetchData() {
    //   get_upload(id.value).then((data) => (upload.value = data));
    // }
    // fetchData();
    return { upload, id };
  },
});
</script>