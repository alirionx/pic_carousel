import Vue from 'vue'
import Vuex from 'vuex'

// import axios from 'axios'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    username: null,
    role: null,
    bearer: null,

    err: false,
    err_msg: null,
    
    active_tab: 0,
    tabs:[
      {
        txt: "Home",
        lnk: "/",
        roles: ["user", "admin"],
        auth: false
      },
      {
        txt: "Carousels",
        lnk: "/carousels",
        roles: ["user", "admin"],
        auth: true
      },
      {
        txt: "Users",
        lnk: "/users",
        roles: ["admin"],
        auth: true
      },
      {
        txt: "Login",
        lnk: "/login",
        roles: ["user", "admin"],
        auth: false
      },
      {
        txt: "Logout",
        func: "logout",
        roles: ["user", "admin"],
        auth: true
      }
    ]
  },
  getters: {
    filtered_tabs(state){
      let tabs = []
      for(let idx in state.tabs){
        if(state.tabs[idx].lnk === '/login' && state.role){
          continue
        }
        else if(!state.tabs[idx].auth){
          tabs.push(state.tabs[idx])
          continue
        }
        else if( state.tabs[idx].roles.includes(state.role) ){
          tabs.push(state.tabs[idx])
          continue
        }
      }
      return tabs
    },

    get_tab_by_lnk: (state) => (lnk)=>{
      return state.tabs.find(tab => tab.lnk === lnk) //AAAAALLLLLTER
    }

  },

  mutations: {
    set_userdata(state, token){
      let tokenData = JSON.parse(atob(token.split('.')[1]));
      state.username = tokenData.username;
      state.role = tokenData.role;
      state.bearer = token;
    },
    reset_userdata(state){
      state.username = null;
      state.role = null;
      state.bearer = null;
    },
    set_active_tab(state, idx){
      state.active_tab = idx;
    },

    set_err(state, msg){
      state.err = true
      state.err_msg = msg
    },
    reset_err(state){
      state.err = false
      state.err_msg = null
    }

  },
  actions: {
    login(context, token){
      localStorage.setItem("bearer", token)
      context.commit('set_userdata', token) // => SAUBER!!!
      // this.state.username = tokenData.username
      // this.state.role = tokenData.role
    },

    logout(context){
      context.commit('reset_userdata')
      localStorage.removeItem("bearer")
      // this.state.username = null
      // this.state.role = null
    },
    
    check_token(context){
      var chk = false
      let token = localStorage.getItem("bearer")
      if(token){
        let tokenData = JSON.parse(atob(token.split('.')[1]));
        let nowTs = Date.now() / 1000 | 0
        if(tokenData.expires > nowTs){
          context.commit('set_userdata', token)
          chk = true
        }
      }
      return chk
    },

    set_active_tab(context){
      for(let idx in this.getters.filtered_tabs){ //UIUIUIUIUIUIU
        if(this.getters.filtered_tabs[idx].lnk == location.hash.substring(1)){
          context.commit('set_active_tab', parseInt(idx)) // => SUBBERSAUBER!!!
          break;
        }
      }
    }
  },
  modules: {
  }
})
