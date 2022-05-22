import { createRouter, createWebHashHistory } from 'vue-router'
import Carousels from '../views/Carousels.vue'
import axios, { Axios } from 'axios'
import store from '../store/index.js'

const routes = [
  {
    path: '/',
    name: 'home',
    component: Carousels,
    meta:{
      auth: true
    }
  },
  {
    path: '/login',
    name: 'login',
    component: function () {
      return import( '../views/Login.vue')
    },
    meta:{
      auth: false
    }
  },
  {
    path: '/carousels',
    name: 'carousels',
    component: function () {
      return import( '../views/Carousels.vue')
    },
    meta:{
      auth: true
    }
  },
  {
    path: '/images',
    name: 'images',
    component: function () {
      return import( '../views/Images.vue')
    },
    meta:{
      auth: true
    }
  },
  {
    path: '/users',
    name: 'users',
    component: function () {
      return import( '../views/Users.vue')
    },
    meta:{
      auth: true
    }
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  let status;
  if(to.meta.auth){

    store.dispatch('check_bearer_state')
      .then((res)=>{
        next()
      })
      .catch((error)=>{
        next("/login")
      })
  }
  else{
    next();
  }

})

export default router
