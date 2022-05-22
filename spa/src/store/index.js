import axios from 'axios'
import { createStore } from 'vuex'

export default createStore({
  state: {
    // bearer: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImRxdWlsaXR6c2NoIiwicm9sZSI6InVzZXIiLCJjcmVhdGVkIjoxNjUyOTkwMTM2LCJleHBpcmVzIjoxNzM5MzkwMTM2fQ.5V9wjTWxkwqT2NllatUV8vPZTRK26TRaQJ4F8LFOmW0",
    bearer: null,
    username: null,
    role: null,
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
      }
    ]
  },
  getters: {
  },
  mutations: {
    set_bearer(bearer){
      this.state.bearer = bearer;
    },
    reset_bearer(){
      this.state.bearer = null;
    }
  },
  actions: {
    check_bearer_state(context){

      return new Promise((resolve, reject) => {
        if(!this.state.bearer){
          reject("no valid login")
        }
        else{
          try {
            const payload = JSON.parse(atob(this.state.bearer.split('.')[1]));
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

    set_bearer(context, bearer){
      // context.commit('set_bearer', bearer)
      this.state.bearer = bearer;
    },

  },
  modules: {
  }
})
