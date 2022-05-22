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
    selectedTab: 0
  }),

  methods:{
    go_to_hash(lnk){
      location.hash = lnk;
    },
    set_tab_by_hash(){
      let curHash = location.hash.replace("#","");
      let defi = this.$store.state.menuDefi;
      for(let idx in defi){
        if(defi[idx].lnk === curHash){
          setTimeout( ()=>{ this.selectedTab = parseInt(idx)}, 200); //EVIL!!!
          // this.selectedTab = parseInt(idx);
          break;
        }
      }
    }
  },
  mounted: function(){
    this.set_tab_by_hash();
  },
  updated: function(){
    
  }
}
</script>
