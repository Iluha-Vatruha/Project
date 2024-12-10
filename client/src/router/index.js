import { createRouter, createWebHistory } from 'vue-router'
import StudentsView from '@/views/StudentsView.vue'
import GroupsView from '@/views/GroupsView.vue'
import SpecialtiesView from '@/views/SpecialtiesView.vue'
import FacultiesView from '@/views/FacultiesView.vue'
import UniversitiesView from '@/views/UniversitiesView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/", 
      name: "StudentsView", 
      component: StudentsView
    },
    {
      path: "/groups", 
      name: "GroupsView", 
      component: GroupsView
    },
    {
      path: "/specialties", 
      name: "SpecialtiesView", 
      component: SpecialtiesView
    },
    {
      path: "/faculties", 
      name: "FacultiesView", 
      component: FacultiesView
    },
    {
      path: "/universities", 
      name: "UniversitiesView", 
      component: UniversitiesView
    }
  ]
})

export default router
