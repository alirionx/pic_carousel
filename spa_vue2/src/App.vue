<template>
  <v-app>
    <v-sheet elevation="6 mb-4" class="purple darken-3" app>
      <v-tabs
        class="px-2"
        background-color="purple darken-3"
        center-active
        dark
        font-white
        right
      >
        <v-tab v-for="(tab,idx) in filtered_tabs()" :key="idx" @click="go_to_lnk(tab)">{{tab.txt}}</v-tab>
      </v-tabs>
  
    </v-sheet>

    <v-main class="ma-2">
      <router-view/>
    </v-main>
  </v-app>
</template>

<script>

export default {
  name: 'App',

  data: () => ({
    msg: "Hallo Welt",
    tabs:[
      {
        txt: "Home",
        lnk: "/",
        roles: []
      },
      {
        txt: "Carousels",
        lnk: "/carousels",
        roles: ["user", "admin"]
      },
      {
        txt: "Users",
        lnk: "/users",
        roles: ["admin"]
      },
      {
        txt: "Login",
        lnk: "/login",
        roles: [null]
      },
      {
        txt: "Logout",
        func: "logout",
        roles: ["user", "admin"]
      }
    ]
  }),
  methods:{

    filtered_tabs(){
      let tabs = []
      for(let idx in this.tabs){
        if(!this.tabs[idx].roles.length){
          tabs.push(this.tabs[idx])
          continue
        }
        else if( this.tabs[idx].roles.includes(this.$store.state.role) ){
          tabs.push(this.tabs[idx])
          continue
        }
      }
      return tabs
    },  

    go_to_lnk(tab){
      if(tab.lnk){
        location.hash = tab.lnk;
      }
      if(tab.func){
        this.$store.dispatch(tab.func).then(location.hash = "/")
      }
    },

  }
};
</script>
