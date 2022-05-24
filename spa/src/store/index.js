// import axios from 'axios'
import { createStore } from 'vuex'

export default createStore({
  state: {
    bearer: null,
    username: null,
    role: null,
    selectedTab: 0,
    menuDefi:[
      {
        txt: "Carousels",
        lnk: "/carousels"
      },
      {
        txt: "Images",
        lnk: "/images"
      },
      {
        txt: "Users",
        lnk: "/users"
      },
      {
        txt: "Logout",
        act: "reset_bearer",
        lnk: "/login"
      }
    ]
  },
  getters: {
  },
  mutations: {

  },
  actions: {
    check_bearer_state(context){
      this.state.bearer = localStorage.getItem("bearer");
      
      let payload;
      if(this.state.bearer){
        payload = JSON.parse(atob(this.state.bearer.split('.')[1]));
        this.state.role = payload.role;
      }
      

      return new Promise((resolve, reject) => {
        if(!this.state.bearer){
          reject("no valid login")
        }
        else{
          try {
            // console.log(payload.expires);
            let now = Date.now() / 1000 | 0
            if(payload.expires > now){
              resolve("valid login");
            }
            else{
              // context.commit('reset_bearer')
              this.state.bearer = null;
              reject("no valid login")
            }
          } 
          catch (e) {
            // context.commit('reset_bearer')
            this.state.bearer = null;
            reject("no valid login")
          }
        }
      })
    },

    set_selected_tab(context, idx){
      this.state.selectedTab = idx;
    },

    set_bearer(context, bearer){
      // context.commit('set_bearer', bearer)
      this.state.bearer = bearer;
      const payload = JSON.parse(atob(bearer.split('.')[1]));
      this.state.role = payload.role;
      localStorage.setItem("bearer", bearer);

    },
    reset_bearer(context){
      this.state.bearer = null;
      this.state.role = null;
      this.state.selectedTab = 0;
      localStorage.removeItem("bearer")
    }

  },
  modules: {
  }
})
