import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Login from '../views/Login.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/login',
    name: 'login',
    component: Login
  },
  {
    path: '/carousels',
    name: 'carousels',
    component: function () {
      return import(/* webpackChunkName: "about" */ '../views/Carousels.vue')
    }
  },
  {
    path: '/users',
    name: 'Users',
    component: function () {
      return import('../views/Users.vue')
    }
  }
]

const router = new VueRouter({
  routes
})

export default router
