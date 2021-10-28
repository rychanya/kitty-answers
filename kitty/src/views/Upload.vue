<template>
  <div class="container">
    <form class="box">
      <div class="file is-fullwidth is-info" :class="{ 'has-name': fileName }">
        <label class="file-label">
          <input
            class="file-input"
            type="file"
            name="resume"
            @change="handleFileUpload($event)"
          />
          <span class="file-cta">
            <span class="file-icon">
              <i class="fas fa-file-excel"></i>
            </span>
            <span class="file-label"> Выберите файл </span>
          </span>
          <span v-if="fileName" class="file-name">{{ fileName }}</span>
        </label>
      </div>
      <div v-if="hasError" class="notification is-danger is-light">
        <ul v-if="hasError">
          <li v-if="!isSizeCorrect">большой</li>
          <li v-if="!isFormatCorrect">формат</li>
        </ul>
      </div>
    </form>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from "vue";
import { upload } from "@/api/search";

export default defineComponent({
  name: "Upload",
  setup() {
    const maxSize = 100 * 1024;
    let file = ref<File>();
    const fileName = computed(() => {
      if (file.value) {
        return file.value.name;
      } else return undefined;
    });
    const isSizeCorrect = computed(() => {
      if (file.value) {
        return file.value.size < maxSize;
      } else return undefined;
    });
    const isFormatCorrect = computed(() => {
      if (file.value) {
        return file.value.name.endsWith(".xlsx");
      } else return undefined;
    });
    const hasError = computed(() => {
      if (file.value) {
        return !isSizeCorrect.value || !isFormatCorrect.value;
      } else return undefined;
    });
    const handleFileUpload = (event: Event) => {
      if (event.target) {
        const target = event.target as HTMLInputElement;
        if (target.files && target.files.length > 0) {
          file.value = target.files[0];
          if (
            file.value &&
            isSizeCorrect.value === true &&
            isFormatCorrect.value === true
          ) {
            upload(file.value).then((v) => console.log(v));
          }
        }
      }
    };
    return {
      handleFileUpload,
      file,
      fileName,
      isSizeCorrect,
      isFormatCorrect,
      hasError,
    };
  },
});
</script>
