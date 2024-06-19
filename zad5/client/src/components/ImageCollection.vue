<script setup>
import {ref, watch} from 'vue'
import ListItem from "@/components/ImageDetails.vue";

const PAGE_SIZE = 5

const page = ref(1)
const length = ref(0)
const images = ref([])
const tag = ref('')

const newImages = ref(0)
let localSnapshot = 0
let localImagesStore = []

async function fetchImages() {
  let url = `http://localhost:8000/images`
  const res = await fetch(url)
  return await res.json()
}

async function fetchImagesAndUpdateState() {
  let resp = await fetchImages()
  let newImages = []
  let count = resp['images'].length

  for (let i = 0; i < count; i++)
    newImages.push(resp['images'][i])
  localImagesStore = newImages
  localSnapshot = resp['snapshot']
  newImages.value = 0

  updateImagesView()
}

async function checkNewImagesAvailability() {
  const resp = await (await fetch(`http://localhost:8000/images/total`)).json();

  if (resp['snapshot'] !== localSnapshot) {
    newImages.value = resp['total_images'] - localImagesStore.length
  }
}

function filterImages() {
  let tagged = localImagesStore
    .filter(img => tag.value === '' || img.tags.some(imgTag => imgTag.startsWith(tag.value)), tag)

  if (page.value * PAGE_SIZE > tagged.length)
    page.value = Math.ceil(tagged.length / PAGE_SIZE)

  return tagged
}

function paginate(images) {
  let lb = (page.value - 1) * PAGE_SIZE
  let ub = Math.min(page.value * PAGE_SIZE, images.length)
  return images.slice(lb, ub)
}

function updateImagesView() {
  let filtered = filterImages()
  images.value = paginate(filtered)
  length.value = Math.ceil(filtered.length / PAGE_SIZE)
}


async function onRefreshClick() {
  const resp = await (await fetch(`http://localhost:8000/images/total`)).json();

  if (resp['snapshot'] !== localSnapshot) {
    await fetchImagesAndUpdateState()
  }
}


setInterval(checkNewImagesAvailability, 5000);

fetchImagesAndUpdateState()
watch(page, updateImagesView)
watch(tag, updateImagesView)

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

