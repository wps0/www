<script setup>
import {ref, watch} from 'vue'
import ListItem from "@/components/ListItem.vue";

const page = ref(1)
const length = ref(0)
const images = ref([])
const tag = ref('')

const newImages = ref(0)
let totalImages = 0
let localSnapshot = 0

async function fetchImages() {
  let url = `http://localhost:8000/images/p/${page.value}`

  if (tag.value !== '') {
    url = `http://localhost:8000/images/p/${page.value}/${tag.value}`
  }

  const res = await fetch(url)

  let resp = await res.json()
  let images_new = []
  for (let i = 0; i < resp['count']; i++)
    images_new.push(resp['images'][i])
  images.value = images_new
  length.value = resp['pages']
  return resp
}

async function firstFetchImages() {
  let resp = await fetchImages()
  length.value = resp['pages']
  newImages.value = 0
}

async function fetchImagesByTag() {
  if (page.value === 1)
    await fetchImages()
  else
    page.value = 1
}

async function fetchNewImages() {
  const resp = await (await fetch(`http://localhost:8000/images/total`)).json();
  if (resp['snapshot'] !== localSnapshot) {
    newImages.value += resp['total_images'] - totalImages
    totalImages = resp['total_images']
    localSnapshot = resp['snapshot']
  }
}


async function onRefreshClick() {
  const resp = await (await fetch(`http://localhost:8000/images/total`)).json();
  totalImages = resp['total_images']
  length.value = resp['pages']
  newImages.value = 0
  page.value = length.value
}

setInterval(fetchNewImages, 5000);

firstFetchImages()
watch(page, fetchImages)
watch(tag, fetchImagesByTag)

</script>


<template>
  <v-container class="fill-height">
    <v-responsive
      class="mx-auto"
      max-width="900"
    >
      <div class="text-center">
        <h1 class="text-h2 font-weight-bold">
          Images
          <v-chip color="primary">
            New: {{ newImages }}
          </v-chip></h1>
      </div>

      <div class="py-4" />

      <input v-model="tag" required placeholder="Enter a tag" />

      <div class="py-4" />

      <v-list lines="two">
        <v-list-item
          v-for="img in images"
          :key="img"
        >
          <ListItem :img="img" />
        </v-list-item>
      </v-list>

      <v-pagination
        :length="length"
        v-model="page">
      </v-pagination>
      <div class="text-center">
        <v-btn @click="onRefreshClick">
          Refresh images
        </v-btn>
      </div>
    </v-responsive>
  </v-container>
</template>

