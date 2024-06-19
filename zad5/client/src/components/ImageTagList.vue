<script>
const props = defineProps({
  tags: Object
})
</script>

<template>
  <br />
  <span v-for="tag in tags"
    :key="tag">
  <v-chip
      class="ma-2"
      color="pink"
      label
  >
    <v-icon icon="mdi-label" start></v-icon>
    {{ tag }}
  </v-chip>
</span>
</template>
