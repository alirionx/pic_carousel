import { createRouter, createWebHashHistory } from 'vue-router'
import Carousels from '../views/Carousels.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: Carousels
  },
  {
    path: '/carousels',
    name: 'carousels',
    component: function () {
      return import( '../views/Carousels.vue')
    }
  },
  {
    path: '/images',
    name: 'images',
    component: function () {
      return import( '../views/Images.vue')
    }
  },
  {
    path: '/users',
    name: 'users',
    component: function () {
      return import( '../views/Users.vue')
    }
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
