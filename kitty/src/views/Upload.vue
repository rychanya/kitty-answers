<template>
  <div class="container">
    <div class="file is-large is-boxed is-centered is-info">
      <label class="file-label">
        <input class="file-input" type="file" name="resume" />
        <span class="file-cta">
          <span class="file-icon">
            <i class="fas fa-file-excel"></i>
          </span>
          <span class="file-label"> Выберите файл </span>
        </span>
      </label>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { upload } from "@/api/search";

export default defineComponent({
  name: "Upload",
  setup() {
    const uploadClick = () => {
      upload().then((v) => console.log(v));
    };
    return { uploadClick };
  },
});
</script>
