<template>
  <v-container fluid>
    <v-card
        max-width="600"
        class="mx-auto"
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
        max-width="205"
        class="mx-auto"
    >
      <v-btn
          :loading="loading"
          :disabled="loading"
          color="primary"
          class="ma-2 white--text"
          @click="overlay = !overlay"
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
      overlay: false,
      // Begin expansion panels params.
      accordion: false,
      popout: true,
      focusable: true,
      // End expansion panels params.
    }
  },
  mounted() {
    this.getCourses();
  },
  watch: {
    overlay(val) {
      val && this.updateCourses()
    },
  },
  methods: {
    getCourses: function () {
      const apiUrl = '/api/course/';
      this.loading = true;
      axios.get(apiUrl)
          .then((response) => {
            this.courses = response.data;
            console.log(response)
            this.loading = false
            this.successHandler('Данные успешно получены!');
          })
          .catch((err) => {
            let msg = {message: 'Не удалось получить данные от сервера' + err};
            this.errorHandler(msg);
            throw msg.message;
          })
    },
    updateCourses: function () {
      const apiUrl = '/update';
      // setTimeout(() => {
      //   this.overlay = false
      // }, 3000)
      this.overlay = true;
      axios.get(apiUrl)
          .then((response) => {
            if (response.status === 200) {
              this.successHandler('Курсы обновлены успешно');
            }
            this.overlay = false
          })
          .catch((err) => {
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