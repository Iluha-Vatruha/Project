<script setup>
import { onBeforeMount, ref, computed} from 'vue';
import axios from 'axios';
import Cookies from 'js-cookie';

onBeforeMount(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
})






const faculties = ref([]);
const facultiesToAdd = ref([]);
const facultiesToEdit = ref([]);

const universities = ref([]);

const loading = ref();

let count = ref();
let most_popular_university = ref();

async function fetchFaculties() {
  loading.value = true;
  const r = await axios.get("/api/faculties/");
  console.log(r.data)
  faculties.value = r.data;
  loading.value = false;  

  const r_stats = await axios.get("/api/faculties/stats/");

  let stats = r_stats.data;
  count.value = stats.count;
  most_popular_university.value = stats.most_popular_university;
}

async function fetchUniversities() {
  loading.value = true;
  const r = await axios.get("/api/universities/");
  console.log(r.data)
  universities.value = r.data;
  loading.value = false;  

  
}



async function onLoadClick() {
  await fetchUniversities()
  await fetchFaculties()
}

onBeforeMount(async () => {
  await fetchUniversities()
  await fetchFaculties()
})

async function onFacultyAdd() {
console.log(facultiesToAdd.value)
  await axios.post("/api/faculties/", {
    ...facultiesToAdd.value,
  });
  await fetchFaculties(); // переподтягиваю
}

async function onRemoveFacultyClick(faculty) {
  await axios.delete(`/api/faculties/${faculty.id}/`);
  await fetchFaculties(); // переподтягиваю
}

async function onFacultyEditClick(faculty) {
  facultiesToEdit.value = { ...faculty };
}

async function onUpdateFaculty() {
  await axios.put(`/api/faculties/${facultiesToEdit.value.id}/`, {
    ...facultiesToEdit.value,
  });
  await fetchFaculties();
}





</script>
<template>
    <form @submit.prevent.stop="onFacultyAdd">
        <div class="row">
        Группы
        </div>
        <div class="row">
            <div class="col">
                <div class="form-floating">
                <!-- ТУТ ПОДКЛЮЧИЛ studentToAdd.name -->
                <input
                    type="text"
                    class="form-control"
                    v-model="facultiesToAdd.name"
                    required
                />
                <label for="floatingInput">Название</label>
                </div>
            </div>
            <div class="col-auto">
                <!-- А ТУТ ПОДКЛЮЧИЛ К select -->
                <div class="form-floating">
                <select class="form-select" v-model="facultiesToAdd.university" required>
                    <option :value="g.id" v-for="g in universities">{{ g.name }}</option>
                </select>
                <label for="floatingInput">Специальность</label>
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
        <h3 class="filterHeader">Статистика по Институтам</h3>
        <div class="col"> Общее количество институтов:
            {{ count }}
        </div>
        <div class="col"> Самый многочисленый университет:
            {{ most_popular_university }}
        </div>
    </div>

    <!-- ТУТ ПОДКЛЮЧИЛ studentToAdd.name -->
    <div v-for="item in faculties" class="faculty-item"> 
        <div class="row rowCool">
            <div class="row colom1">
                <div class="col">{{ item.name }}</div>
                <div class="col">{{ item.university.name }}</div>
            </div>
            <div class="col-auto colom3">
                <button class="btn btn-danger" @click="onRemoveFacultyClick(item)">
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
                @click="onFacultyEditClick(item)"
                data-bs-toggle="modal"
                data-bs-target="#editFacultyModal"
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
    <div class="modal fade" id="editFacultyModal" tabindex="-1">
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
                                v-model="facultiesToEdit.name"
                                />
                                <label for="floatingInput">Название</label>
                            </div>
                        </div>
                        <div class="col-auto">
                            <div class="form-floating">
                                <select class="form-select" v-model="facultiesToEdit.university">
                                <option :value="g.id" v-for="g in universities">
                                    {{ g.name }}
                                </option>
                                </select>
                                <label for="floatingInput">Специальность</label>
                            </div>
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
                        @click="onUpdateFaculty"
                    >
                        Сохранить
                    </button>
                </div>
            </div>
        </div>
    </div>
  
</template>

<style scoped>
    .colom1{
        width: 80%;
    }
    .colom2{
        width: 30%;
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
</style>