<script setup>
import {computed, ref, onBeforeMount} from 'vue';
import axios from "axios";
import Cookies from 'js-cookie';
import { storeToRefs } from 'pinia';
import useUserProfileStore from '@/stores/UseProfileStore';

const userProfileStore = useUserProfileStore();
const {
  is_auth, 
  username, 
  is_superuser
} = storeToRefs(userProfileStore);

onBeforeMount(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
})

const students = ref([]);
const studentToAdd = ref({});
const studentToEdit = ref({});

const studentsPictureRef = ref();
const studentAddImageUrl = ref()
const studentEditImageUrl = ref()
const studentPictureRefForEdit = ref();

let isEnlargedImg = ref(false);
let currentImgSrc = ref("");
let box = ref();
let img = ref();

let userToFilt = ref();

let usersToFilter = ref([]);
const allUsers = "Все";



const groups = ref([]);

const loading = ref();

let count = ref();
let most_popular_group = ref();

async function fetchStudents() {
  loading.value = true;
  const r = await axios.get("/api/students/");
  console.log(r.data)
  students.value = r.data;
  loading.value = false;

  let users = students.value.map(student => student.username);
  users = users.filter(user => user != null);
  usersToFilter = Array.from(new Set(users));
  usersToFilter.unshift(allUsers); 

  const r_stats = await axios.get("/api/students/stats/");

  let stats = r_stats.data;
  count = stats.count;
  most_popular_group = stats.most_popular_group;
}

async function fetchGroups() {
  loading.value = true;
  const r = await axios.get("/api/groups/");
  console.log(r.data)
  groups.value = r.data;
  loading.value = false;  
}


async function onLoadClick() {
  await fetchStudents()
  await fetchGroups()
}

onBeforeMount(async () => {
  await fetchStudents()
  await fetchGroups()
  if (!is_superuser.value)
  {
    userToFilt = allUsers;
  }
})

async function onStudentAdd() {
    const formData = new FormData();
    
    if(studentsPictureRef.value.files.length > 0){
        formData.append('picture', studentsPictureRef.value.files[0]);
    }

    formData.set('name', studentToAdd.value.name)
    formData.set('group', studentToAdd.value.group)

  await axios.post("/api/students/", formData, {
    headers: {
        'Content-Type': 'multipart/form-data'
    }
  });
  await fetchStudents(); // переподтягиваю
}

async function studentAddPictureChange() {
    studentAddImageUrl.value = URL.createObjectURL(studentsPictureRef.value.files[0])
}
async function studentEditPictureChange()
{
    studentEditImageUrl.value = URL.createObjectURL(studentPictureRefForEdit.value.files[0]);
}

async function onRemoveStudentClick(student) {
  await axios.delete(`/api/students/${student.id}/`);
  await fetchStudents(); // переподтягиваю
}


async function onStudentEditClick(student) {
  studentToEdit.value = { ...student };
}


async function onUpdateStudent() {

    const formData = new FormData();
    
    if(studentPictureRefForEdit.value.files.length > 0){
        formData.append('picture', studentPictureRefForEdit.value.files[0]);
    }

    formData.set('name', studentToEdit.value.name)
    formData.set('group', studentToEdit.value.group)

  await axios.put(`/api/students/${studentToEdit.value.id}/`, formData, {
    headers: {
        'Content-Type': 'multipart/form-data'
    }});
  await fetchStudents();
}
function onZoomBoxClick()
{
    isEnlargedImg.value = false;
}
function onImgClick(item)
{
  isEnlargedImg.value = true;
  currentImgSrc.value = item.picture;
}


</script>
<template>
    <Transition>
        <div v-if="isEnlargedImg" id="zoomBox" class="zoomedBox" @click="onZoomBoxClick">
            <img id="zoomedImg" :src="currentImgSrc" class="enlarged" alt="">
        </div>
    </Transition>
    <div class="container-fluid">
        <form @submit.prevent.stop="onStudentAdd">
            <div class="row">
            Студенты
            </div>
            <div class="row">
                <div class="col">
                    <div class="form-floating">
                        <input
                            type="text"
                            class="form-control"
                            v-model="studentToAdd.name"
                            required
                        />
                        <label for="floatingInput">ФИО</label>
                    </div>
                </div>
                <div class="col-auto">
                    <input class="form-control" type="file" ref="studentsPictureRef" @change="studentAddPictureChange">
                </div>
                <div class="col-auto">
                    <img :src="studentAddImageUrl" style="max-height: 60px;" alt="">
                </div>
                <div class="col-auto">
                    <!-- А ТУТ ПОДКЛЮЧИЛ К select -->
                    <div class="form-floating">
                        <select class="form-select" v-model="studentToAdd.group" required>
                            <option :value="g.id" v-for="g in groups">{{ g.name }}</option>
                        </select>
                        <label for="floatingInput">Группа</label>
                    </div>
                </div>
                <div class="col-auto">
                    <button class="btn btn-primary">
                    Добавить
                    </button>
                </div>
            </div>
        </form>
        <div>
            <h3 class="filterHeader">Статистика по студентам</h3>
            <div class="col"> Общее количество студентов:
               {{ count }}
            </div>
            <div class="col"> Самая многочисленная группа:
               {{ most_popular_group }}
            </div>
        </div>
        <div v-if="is_superuser">
            <h3 class="filterHeader">Фильтрация по пользователю</h3>
            <div class="col-2 selectUser">
                <div class="form-floating">
                    <select class="form-select" v-model="userToFilt">
                        <option :value="user" v-for="user in usersToFilter">{{ user }}</option>
                    </select>
                    <label for="floatingInput">Пользователь</label>
                </div>
            </div>
        </div>

        <div v-if="!is_superuser">
            <div v-for="item in students" class="student-item"> 
                <div class="row rowCool">
                    <div class="row colom1">
                        <div class="col">{{ item.name }}</div>
                        <div class="col">{{ item.group.name }}</div>
                    </div>
                    <div class="col-auto colom2">
                        <div v-show="item.picture">
                            <img :src="item.picture" style="max-height: 60px;" @click="onImgClick(item)"> 
                        </div>
                    </div>
                    <div class="col-auto colom3">
                        <button class="btn btn-danger" @click="onRemoveStudentClick(item)">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash3-fill" viewBox="0 0 16 16">
                                <path d="M11 1.5v1h3.5a.5.5 0 0 1 0 1h-.538l-.853 10.66A2 2 0 0 1 11.115 16h-6.23a2 2 0 0 1-1.994-1.84L2.038 
                                3.5H1.5a.5.5 0 0 1 0-1H5v-1A1.5 1.5 0 0 1 6.5 0h3A1.5 1.5 0 0 1 11 1.5m-5 0v1h4v-1a.5.5 0 0 0-.5-.5h-3a.5.5 
                                0 0 0-.5.5M4.5 5.029l.5 8.5a.5.5 0 1 0 .998-.06l-.5-8.5a.5.5 0 1 0-.998.06m6.53-.528a.5.5 0 0 0-.528.47l-.5 
                                8.5a.5.5 0 0 0 .998.058l.5-8.5a.5.5 0 0 0-.47-.528M8 4.5a.5.5 0 0 0-.5.5v8.5a.5.5 0 0 0 1 0V5a.5.5 0 0 0-.5-.5"/>
                            </svg><i class="bi bi-x"></i>
                        </button>
                    </div>
                    <div class="col-auto colom4">
                        <button
                            class="btn btn-success"
                            @click="onStudentEditClick(item)"
                            data-bs-toggle="modal"
                            data-bs-target="#editStudentModal"
                            >
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil-square" viewBox="0 0 16 16">
                            <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0
                            0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"/>
                            <path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 
                            1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5z"/>
                            </svg>
                            <i class="bi bi-pen-fill"></i>
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <div v-else>
            <div v-if="userToFilt != allUsers">
                <div v-for="item in students">
                    <div v-if="item.username == userToFilt">
                        <div class="row rowCool">
                            <div class="row colom1">
                                <div class="col">{{ item.name }}</div>
                                <div class="col">{{ item.group.name }}</div>
                            </div>
                            <div class="col-auto colom2">
                                <div v-show="item.picture">
                                    <img :src="item.picture" style="max-height: 60px;" @click="onImgClick(item)"> 
                                </div>
                            </div>
                            <div class="col-auto colom3">
                                <button class="btn btn-danger" @click="onRemoveStudentClick(item)">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash3-fill" viewBox="0 0 16 16">
                                        <path d="M11 1.5v1h3.5a.5.5 0 0 1 0 1h-.538l-.853 10.66A2 2 0 0 1 11.115 16h-6.23a2 2 0 0 1-1.994-1.84L2.038 
                                        3.5H1.5a.5.5 0 0 1 0-1H5v-1A1.5 1.5 0 0 1 6.5 0h3A1.5 1.5 0 0 1 11 1.5m-5 0v1h4v-1a.5.5 0 0 0-.5-.5h-3a.5.5 
                                        0 0 0-.5.5M4.5 5.029l.5 8.5a.5.5 0 1 0 .998-.06l-.5-8.5a.5.5 0 1 0-.998.06m6.53-.528a.5.5 0 0 0-.528.47l-.5 
                                        8.5a.5.5 0 0 0 .998.058l.5-8.5a.5.5 0 0 0-.47-.528M8 4.5a.5.5 0 0 0-.5.5v8.5a.5.5 0 0 0 1 0V5a.5.5 0 0 0-.5-.5"/>
                                    </svg><i class="bi bi-x"></i>
                                </button>
                            </div>
                            <div class="col-auto colom4">
                                <button
                                    class="btn btn-success"
                                    @click="onStudentEditClick(item)"
                                    data-bs-toggle="modal"
                                    data-bs-target="#editStudentModal"
                                    >
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil-square" viewBox="0 0 16 16">
                                    <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0
                                    0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"/>
                                    <path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 
                                    1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5z"/>
                                    </svg>
                                    <i class="bi bi-pen-fill"></i>
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div v-else>
                <div v-for="item in students" class="student-item"> 
                    <div class="row rowCool">
                        <div class="row colom1">
                            <div class="col">{{ item.name }}</div>
                            <div class="col">{{ item.group.name }}</div>
                        </div>
                        <div class="col-auto colom2">
                            <div v-show="item.picture">
                                <img :src="item.picture" style="max-height: 60px;" @click="onImgClick(item)"> 
                            </div>
                        </div>
                        <div class="col-auto colom3">
                            <button class="btn btn-danger" @click="onRemoveStudentClick(item)">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash3-fill" viewBox="0 0 16 16">
                                    <path d="M11 1.5v1h3.5a.5.5 0 0 1 0 1h-.538l-.853 10.66A2 2 0 0 1 11.115 16h-6.23a2 2 0 0 1-1.994-1.84L2.038 
                                    3.5H1.5a.5.5 0 0 1 0-1H5v-1A1.5 1.5 0 0 1 6.5 0h3A1.5 1.5 0 0 1 11 1.5m-5 0v1h4v-1a.5.5 0 0 0-.5-.5h-3a.5.5 
                                    0 0 0-.5.5M4.5 5.029l.5 8.5a.5.5 0 1 0 .998-.06l-.5-8.5a.5.5 0 1 0-.998.06m6.53-.528a.5.5 0 0 0-.528.47l-.5 
                                    8.5a.5.5 0 0 0 .998.058l.5-8.5a.5.5 0 0 0-.47-.528M8 4.5a.5.5 0 0 0-.5.5v8.5a.5.5 0 0 0 1 0V5a.5.5 0 0 0-.5-.5"/>
                                </svg><i class="bi bi-x"></i>
                            </button>
                        </div>
                        <div class="col-auto colom4">
                            <button
                                class="btn btn-success"
                                @click="onStudentEditClick(item)"
                                data-bs-toggle="modal"
                                data-bs-target="#editStudentModal"
                                >
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil-square" viewBox="0 0 16 16">
                                <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0
                                0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"/>
                                <path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 
                                1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5z"/>
                                </svg>
                                <i class="bi bi-pen-fill"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="modal fade" id="editStudentModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h1 class="modal-title fs-5" id="exampleModalLabel">
                            редактировать
                        </h1>
                        <button
                            type="button"
                            class="btn-close"
                            data-bs-dismiss="modal"
                            aria-label="Close"
                        ></button>
                    </div>
                    <div class="modal-body">
                        <div class="row">
                            <div class="col">
                                <div class="form-floating">
                                    <input
                                    type="text"
                                    class="form-control"
                                    v-model="studentToEdit.name"
                                    />
                                    <label for="floatingInput">Фио</label>
                                </div>
                            </div>
                            <div class="col-auto">
                                <div class="form-floating">
                                    <select class="form-select" v-model="studentToEdit.group">
                                    <option :value="g.id" v-for="g in groups">
                                        {{ g.name }}
                                    </option>
                                    </select>
                                    <label for="floatingInput">Группа</label>
                                </div>
                            </div>
                            <div class="col-auto">
                                <input class="form-control" type="file" ref="studentPictureRefForEdit" @change="studentEditPictureChange">
                            </div>
                            <div class="col-auto">
                                <img :src="studentEditImageUrl" style="max-height: 60px" alt="">
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button
                            type="button"
                            class="btn btn-secondary"
                            data-bs-dismiss="modal"
                        >
                            Close
                        </button>
                        <button
                            data-bs-dismiss="modal"
                            type="button"
                            class="btn btn-primary"
                            @click="onUpdateStudent"
                        >
                            Сохранить
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
    .colom1{
        width: 60%;
    }
    .colom2{
        width: 20%;
        justify-content: center;
    }
    .colom3{
        width: 10%;
    }
    .colom4{    
        width: 10%;
    }
    .rowCool{
        display: flex;
        align-items: center;
        padding: 15px;
        border-radius: 5px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); /* Тень для большей выразительности */
        background-color: #f9f9f9; /* Светлый фон */
        margin-bottom: 10px;
        margin-top: 10px;
    }

    .zoomedBox{
        opacity: 1;
        transform: scale(1, 1);
        height: auto;

        overflow: hidden;
        display: flex;

        position: fixed;
        left: 0;
        right: 0;
        bottom: 0;
        top: 0;
        backdrop-filter: blur(3px);
        z-index: 1000;
        align-items: center;
        justify-content: center;

    }
    .enlarged {
        max-width: 100%;
        z-index: 1000; /* Устанавливаем высокий z-index, чтобы изображение было поверх других элементов */
    }

    .enlarged img {
        max-width: 100%; /* Масштабируем изображение, чтобы оно занимало всю доступную ширину */
        max-height: 100%; /* Масштабируем изображение, чтобы оно занимало всю доступную высоту */
    }
</style>