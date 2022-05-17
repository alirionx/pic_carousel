<template>
  <v-app>
    <v-app-bar app color="purple darken-4" >
      <v-app-bar-title>
        <strong class="subheading">{{title}}</strong>
      </v-app-bar-title>
      <v-tabs v-model="selectedTab" class="pa-3">
        <v-tab 
          v-for="(item,idx) in $store.state.menuDefi" 
          :key="idx"
          @click="go_to_hash(item.lnk)">{{item.txt}}</v-tab>

      </v-tabs>
    </v-app-bar>
    <v-main>
      <router-view/>
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: 'App',
  components: {
  },

  data: () => ({
    title: "Pic Carousel",
    selectedTab: null
  }),

  methods:{
    go_to_hash(lnk){
      location.hash = lnk;
    }
  },
  mounted: function(){
    // console.log(location.hash);
    let curHash = location.hash.replace("#","");
    let defi = this.$store.state.menuDefi;
    for(let idx in defi){
      if(defi[idx].lnk === curHash){
        const callback = ()=>{ this.selectedTab = parseInt(idx);} 
        setTimeout( callback, 500);
        break;
      }
    }
  }
}
</script>
