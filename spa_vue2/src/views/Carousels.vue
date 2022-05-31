<template>
  <div class="Carousels">
    <h1>This is an {{title}} page</h1>
    <v-btn primary @click="call_bearer_from_localstorage">check</v-btn>
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
      call_bearer_from_localstorage(){
        console.log(localStorage.getItem("bearer"))
        let test = this.$store.getters.get_tab_by_lnk('/users').roles
        console.log(test)
      }
    },
    mounted: function(){

    }
  }
</script>