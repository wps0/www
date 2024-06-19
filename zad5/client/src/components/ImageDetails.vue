<script setup>

import {ref} from "vue";
import ImageTagList from "@/components/ImageTagList.vue";

const props = defineProps({
  img: Object
})

const isLoading = ref(false)
const error = ref('')


function onLoadStart() {
  isLoading.value = true
  error.value = ''
}

function onLoad() {
  isLoading.value = false
}

function onError() {
  isLoading.value = false
  error.value = 'error!'
}
</script>

<template>
  <div class="text-center">
    <v-dialog max-width="500">
      <template v-slot:activator="{ props: activatorProps }">
        <v-btn
          v-bind="activatorProps"
          color="surface-variant"
          :text="img.title"
          variant="flat"
        ></v-btn>
      </template>

      <template v-slot:default="{ isActive }">
        <v-card :title="img.title">
          <v-card-text>
            <v-img :src="img.src" @load="onLoad" @loadstart="onLoadStart" @error="onError" />
            <p v-if="isLoading">Loading...</p>
            {{ error }}
          </v-card-text>

          <v-card-actions>
            <v-spacer></v-spacer>

            <v-btn
              text="Close Dialog"
              @click="isActive.value = false"
            ></v-btn>
          </v-card-actions>
        </v-card>
      </template>
    </v-dialog>

    <ImageTagList tags="img.tags" />
  </div>

</template>

