<template>
  <v-app >
    <v-app-bar color="purple darken-4">
      {{title}}
    </v-app-bar>
  </v-app>
</template>

<script>

export default {
  name: 'HeadBlock',

  data: () => ({
    title: "Pic Carousel"
  }),
}
</script>
