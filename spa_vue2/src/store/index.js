import Vue from 'vue'
import Vuex from 'vuex'

// import axios from 'axios'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    username: null,
    role: null,
    bearer: null
  },
  getters: {
  },
  mutations: {
    set_userdata(state, payload){
      state.username = payload.username;
      state.role = payload.role;
      state.bearer = payload.bearer;
    },
    reset_userdata(state){
      state.username = null;
      state.role = null;
      state.bearer = null;
    },

  },
  actions: {
    login(context, token){
      let tokenData = JSON.parse(atob(token.split('.')[1]));
      console.log(tokenData)
      
      let payload = {
        bearer: token,
        username: tokenData.username,
        role: tokenData.role
      }
      context.commit('set_userdata', payload) // => SAUBER!!!
      // this.state.username = tokenData.username
      // this.state.role = tokenData.role
    },

    logout(context){
      context.commit('reset_userdata')
      // this.state.username = null
      // this.state.role = null
    }
  },
  modules: {
  }
})
