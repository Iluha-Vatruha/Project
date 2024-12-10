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


async function fetchUniversities() {
  loading.value = true;
  const r = await axios.get("/api/universities/");
  console.log(r.data)
  universities.value = r.data;
  loading.value = false;  
}

async function fetchFaculties() {
  loading.value = true;
  const r = await axios.get("/api/faculties/");
  console.log(r.data)
  faculties.value = r.data;
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
    <div class="container-fluid">
        <form @submit.prevent.stop="onFacultyAdd">
            <div class="row">
            Институты
            </div>
            <div class="row">
            <div class="col">
                <div class="form-floating">
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
                    <label for="floatingInput">Университет</label>
                </div>
            </div>
            <div class="col-auto">
                <button class="btn btn-primary">
                Добавить
                </button>
            </div>
            
            </div>
        </form>


        <!-- ТУТ ПОДКЛЮЧИЛ studentToAdd.name -->
        <div v-for="item in faculties" class="faculty-item"> 
            <div>{{ item.name }}</div>
            <button class="btn btn-danger" @click="onRemoveFacultyClick(item)">Удалить<i class="bi bi-x"></i>
            </button>
            <button
            class="btn btn-success"
            @click="onFacultyEditClick(item)"
            data-bs-toggle="modal"
            data-bs-target="#editFacultyModal"
            >Редактировать
            <i class="bi bi-pen-fill"></i>
            </button>
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
                                    <label for="floatingInput">Университет</label>
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
    </div>
</template>

<style scoped>
</style>