<template>
  <v-app>
    <v-app-bar app color="purple darken-4" >
      <v-app-bar-title>
        <strong class="subheading">{{title}}</strong>
      </v-app-bar-title>
      <v-tabs v-model="$store.state.selectedTab" class="pa-3" v-if="$store.state.role">
        <v-tab 
          v-for="(item,idx) in $store.state.menuDefi" 
          :key="idx"
          @click="go_to_hash(item)">{{item.txt}}</v-tab>

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
    title: "Pic Carousel"
  }),

  methods:{
    go_to_hash(item){
      if(item.act){
        this.$store.dispatch(item.act);
      }
      location.hash = item.lnk;
    },
    get_idx_of_hash(){
      let curHash = location.hash.replace("#","");
      let defi = this.$store.state.menuDefi;
      let res = 0;
      for(let idx in defi){
        if(defi[idx].lnk === curHash){
          res = parseInt(idx);
          break;
        }
      }
      return res;
    },
    set_tab_by_hash(){
      let idx = this.get_idx_of_hash()
      setTimeout( ()=>{ this.$store.dispatch("set_selected_tab", idx)}, 200); //EVIL!!!
    },

  },
  mounted: function(){
    this.set_tab_by_hash();
  },
  updated: function(){
    
  }
}
</script>
