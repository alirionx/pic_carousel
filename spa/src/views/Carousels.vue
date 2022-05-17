<template>
  <v-card class="pa-4 ma-4 elevation-4">
    {{title}}
  </v-card>
</template>

<script>
import { defineComponent } from 'vue';

// Components
// import HelloWorld from '../components/HelloWorld.vue';

export default defineComponent({
  name: 'Carousels',
  data: () =>({
    title: 'Carousels'
  }),
  components: {
  
  },
  
});
</script>
