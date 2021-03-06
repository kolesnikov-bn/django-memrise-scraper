import Vue from 'vue'
import VueRouter from 'vue-router'
import Courses from '../views/Courses.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Courses',
    component: Courses
  },
  {
    path: '/duplicates',
    name: 'Duplicates',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/Duplicate.vue')
  }
]

const router = new VueRouter({
  routes
})

export default router
