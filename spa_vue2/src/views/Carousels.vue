<template>
  <div class="Carousels">
    <h1>This is an {{title}} page</h1>
  </div>
</template>


<script>
  // import HelloWorld from '../components/HelloWorld'
  import axios from 'axios'

  export default {
    name: 'Carousels',
    data: () => ({
      title: "Carousels"
    }),
    components: {
      
    },
    methods:{

    },
    mounted: function(){

    }
  }
</script>