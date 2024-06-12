<template>
  <v-container class="fill-height">
    <v-responsive
      class="mx-auto"
      max-width="900"
    >
      <div class="text-center">
        <h1 class="text-h2 font-weight-bold">Images</h1>
      </div>

      <div class="py-4" />

      <input v-model="tag" required placeholder="Enter a tag" />

      <div class="py-4" />

      <v-list lines="two">
        <v-list-item
          v-for="img in images"
          :key="img"
        >
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
                    <v-img :src="img.src" @load="isLoading = false" />
                    <p v-if="isLoading">Loading...</p>
                  </v-card-text>

                  <v-card-actions>
                    <v-spacer></v-spacer>

                    <v-btn
                      text="Close Dialog"
                      @click="() => {isActive.value = false; isLoading.value = true}"
                    ></v-btn>
                  </v-card-actions>
                </v-card>
              </template>
            </v-dialog>

            <br />
            <small>
              tags:
              <span v-for="tag in img.tags"
                    :key="tag">
                {{ tag }},
              </span>
            </small>
          </div>
        </v-list-item>
      </v-list>

      <v-pagination
        :length="length"
        v-model="page">
      </v-pagination>
    </v-responsive>
  </v-container>
</template>

<script setup>
import {ref, watch} from 'vue'

  const isLoading = ref(true)
  const page = ref(1)
  const length = ref(0)
  const images = ref([])
  const tag = ref('')

  async function fetchImages() {
    let url = `http://localhost:8000/images/${page.value}`

    if (tag.value !== '') {
      url = `http://localhost:8000/images/${page.value}/${tag.value}`
    }

    const res = await fetch(url)

    let resp = await res.json()
    let images_new = []
    for (let i = 0; i < resp['count']; i++) {
      images_new.push(resp['images'][i])
    }
    images.value = images_new
    length.value = resp['pages']
    console.log(length.value)
  }

  async function fetchImagesByTag() {
    if (page.value === 1)
      await fetchImages()
    else
      page.value = 1
  }

  fetchImages()
  watch(page, fetchImages)
  watch(tag, fetchImagesByTag)

</script>
