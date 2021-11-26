<template><div class="bg-green-500">Ab</div></template>
<script setup lang="ts">
import axios from "axios"

axios.get("/api/qa/6142ca7c3ece906b452d137b").then(data => console.log(data))

</script>