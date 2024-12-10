<script setup>
import {computed, ref, onBeforeMount} from 'vue';
import axios from "axios";
import Cookies from 'js-cookie';

onBeforeMount(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
})

const universities = ref([]);
const universitiesToAdd = ref({});
const universitiesToEdit = ref({});

const loading = ref();

const universityPictureRef = ref();
const universityAddImageUrl = ref()
const universityEditImageUrl = ref()
const universityPictureRefForEdit = ref();

let isEnlargedImg = ref(false);
let currentImgSrc = ref("");
let box = ref();
let img = ref();

let universities_stats_by_names = ref([])

async function fetchUniversities() {
  loading.value = true;
  const r = await axios.get("/api/universities/");
  console.log(r.data)
  universities.value = r.data;
  loading.value = false;

  const r_stats = await axios.get("/api/universities/stats/");

  universities_stats_by_names.value = r_stats.data;

}

async function onLoadClick() {
  await fetchStudents()
  await fetchGroups()
}

onBeforeMount(async () => {
  await fetchUniversities()
})

async function onUniversityAdd() {
    const formData = new FormData();
    if(universityPictureRef.value.files.length > 0){
        formData.append('picture', universityPictureRef.value.files[0]);
    }
    

    formData.set('name', universitiesToAdd.value.name)

  await axios.post("/api/universities/", formData, {
    headers: {
        'Content-Type': 'multipart/form-data'
    }
  });
  await fetchUniversities(); // переподтягиваю
}


async function onRemoveUniversityClick(university) {
  await axios.delete(`/api/universities/${university.id}/`);
  await fetchUniversities(); // переподтягиваю
}


async function onUniversityEditClick(university) {
  universitiesToEdit.value = { ...university };
}


async function onUpdateUniversity() {

    const formData = new FormData();
    if(universityPictureRefForEdit.value.files.length > 0){
        formData.append('picture', universityPictureRefForEdit.value.files[0]);
    }

    formData.set('name', universitiesToEdit.value.name)

  await axios.put(`/api/universities/${universitiesToEdit.value.id}/`, formData, {
    headers: {
        'Content-Type': 'multipart/form-data'
    }});
  await fetchUniversities();
}

async function universityAddPictureChange() {
    universityAddImageUrl.value = URL.createObjectURL(universityPictureRef.value.files[0])
}
async function universityEditPictureChange()
{
    universityEditImageUrl.value = URL.createObjectURL(universityPictureRefForEdit.value.files[0]);
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
        <form @submit.prevent.stop="onUniversityAdd">
            <div class="row">
            Университеты
            </div>
            <div class="row">
            <div class="col">
                <div class="form-floating">
                    <input
                        type="text"
                        class="form-control"
                        v-model="universitiesToAdd.name"
                        required
                    />
                    <label for="floatingInput">Название</label>
                </div>
            </div>
            <div class="col-auto">
                    <input class="form-control" type="file" ref="universityPictureRef" @change="universityAddPictureChange">
                </div>
                <div class="col-auto">
                    <img :src="universityAddImageUrl" style="max-height: 60px;" alt="">
                </div>
            <div class="col-auto">
                <button class="btn btn-primary">
                Добавить
                </button>
            </div>
            
            </div>
        </form>

        <div class="row">
            <div class="col">
                <h3 class="filterHeader">Статистика по университетам</h3>
                <div class="statsRow">
                    <div v-for="item in universities_stats_by_names">
                    <div class="row-aline">
                        <div class="col-name">Название:
                            {{ item.university_name }}
                        </div>
                        <div class="col-amount">Количество студентов:
                            {{ item.student_count }}
                        </div> 
                    </div>
                </div>
                </div>
                
            </div>
            
        </div>

        <div v-for="item in universities" class="university-item"> 
            <div class="row rowCool">
                <div class="row colom1">
                    <div class="col">{{ item.name }}</div>
                </div>
                <div class="col-auto colom2">
                    <div v-show="item.picture">
                        <img :src="item.picture" style="max-height: 60px;" @click="onImgClick(item)"> 
                    </div>
                </div>
                <div class="col-auto colom3">
                    <button class="btn btn-danger" @click="onRemoveUniversityClick(item)">
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
                        @click="onUniversityEditClick(item)"
                        data-bs-toggle="modal"
                        data-bs-target="#editUniversityModal"
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
        <div class="modal fade" id="editUniversityModal" tabindex="-1">
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
                                    v-model="universitiesToEdit.name"
                                    />
                                    <label for="floatingInput">Название</label>
                                </div>
                            </div>
                            <div class="col-auto">
                                <input class="form-control" type="file" ref="universityPictureRefForEdit" @change="universityEditPictureChange">
                            </div>
                            <div class="col-auto">
                                <img :src="universityEditImageUrl" style="max-height: 60px" alt="">
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
                            @click="onUpdateUniversity"
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
    .filterHeader {
    text-align: center;
    margin-bottom: 1.5rem;
    font-size: 1.5rem;
    font-weight: bold;
    color: #333; /* Dark gray header text */
    }

    .row-aline {
        margin: 20px;
        padding: 40px;
        border-radius: 15px;
        width: 25%;
        min-width: 300px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        background-color: #00CED1;
    }

    .col-name {
    width: 30%;
    flex: 1; /* Takes available space */
    font-weight: bold;
    text-align: center;
    color: #000000; /* Slightly darker gray for names */
    }

    .col-amount {
    width: 70%;
    flex: 1;
    font-weight: bold;
    text-align: center; /* Aligns numbers to the right */
    color: #f9f9f9; /* Green for student count */ /* You can change this color */
    }
    .statsRow{
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: center;
    }
</style>