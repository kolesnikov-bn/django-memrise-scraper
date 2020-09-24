<template>
  <v-container fluid>
    <v-card
        flat
        class="d-flex justify-space-around mb-6"
        height="720"
    >
      <v-card
          max-width="600"
          class="d-flex justify-space-around mb-6"
      >
        <v-expansion-panels
            :accordion="accordion"
            :popout="popout"
            :focusable="focusable"
        >
          <v-expansion-panel
              v-for="course in courses"
              :key="course.id"
          >
            <v-expansion-panel-header>
              {{ course.name }}
            </v-expansion-panel-header>
            <v-expansion-panel-content>
              ID: {{ course.id }}
              <v-divider></v-divider>
              LEVELS: {{ course.num_levels }}
              <v-divider></v-divider>
              WORDS: {{ course.num_things }}
            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-expansion-panels>

      </v-card>
      <v-card
          class="justify-space-around" width="790" height="696"
      >
        <v-card-title>
          Words
          <v-spacer></v-spacer>
          <v-text-field
              v-model="search"
              append-icon="mdi-magnify"
              label="Search"
          ></v-text-field>
        </v-card-title>
        <v-data-table
            :headers="headers"
            :items="words"
            :items-per-page.sync="itemsPerPage"
            :search="search"
            :loading="loading"
            :loading-text="loadingText"
            height="530"
        >
        </v-data-table>

      </v-card>
    </v-card>
    <v-card max-width="205" class="mx-auto">
      <v-btn
          color="primary"
          class="ma-2 white--text"
          @click.prevent="updateCourses()"
      >
        Update Courses
        <v-icon right dark>mdi-cloud-upload</v-icon>
      </v-btn>
      <v-overlay :value="overlay">
        <v-progress-circular indeterminate size="64"></v-progress-circular>
      </v-overlay>
    </v-card>
    <v-snackbar
        :timeout="timeout"
        :bottom="position"
        :color="snackColor"
        v-model="snackbar">
      {{ message }}
    </v-snackbar>
  </v-container>
</template>

<script>
import axios from 'axios'
import Helpers from '../helpers'

export default {
  name: "Courses",
  mixins: [Helpers],
  data: function () {
    return {
      courses: [],
      words: [],
      overlay: false,
      // Begin expansion panels params.
      accordion: false,
      popout: true,
      focusable: true,
      // End expansion panels params.
      // Begin Data tables params.
      search: '',
      loading: false,
      loadingText: 'Loading... Please wait',
      itemsPerPage: -1,
      headers: [
        {text: 'WORD A', value: 'word_a'},
        {text: 'WORD B', value: 'word_b'},
        {text: 'COURSE', value: 'level'},
        {text: 'LEVEL', value: 'level_number'},
      ]
      // End Data tables params.
    }
  },
  mounted() {
    this.getCourses();
    this.getWords();
  },
  methods: {
    getCourses: function () {
      const apiUrl = '/api/course/';
      this.overlay = true;
      axios.get(apiUrl)
          .then((response) => {
            this.courses = response.data;
            console.log(response)
            this.overlay = false
            this.successHandler('Данные успешно получены!');
          })
          .catch((err) => {
            this.overlay = false;
            let msg = {message: 'Не удалось получить данные от сервера' + err};
            this.errorHandler(msg);
            throw msg.message;
          })
    },
    getWords: function () {
      const apiUrl = '/api/word/';
      this.overlay = true;
      this.loading = true;
      axios.get(apiUrl)
          .then((response) => {
            this.words = response.data;
            console.log(response)
            this.loading = false
            this.successHandler('Данные успешно получены!');
          })
          .catch((err) => {
            this.loading = false;
            let msg = {message: 'Не удалось получить данные от сервера' + err};
            this.errorHandler(msg);
            throw msg.message;
          })
    },
    updateCourses: function () {
      const apiUrl = '/update';
      this.overlay = true;
      axios.get(apiUrl, {timeout: 1000 * 60 * 5})
          .then((response) => {
            if (response.status === 200) {
              this.successHandler('Курсы обновлены успешно');
            }
            this.overlay = false
          })
          .catch((err) => {
            this.overlay = false;
            let msg = {message: err};
            this.errorHandler(msg);
            throw msg.message;
          })
    }
  }
}
</script>

<style scoped>

</style>