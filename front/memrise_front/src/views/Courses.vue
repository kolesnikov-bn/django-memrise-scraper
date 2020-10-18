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
            <v-expansion-panel-header  v-bind:class="{ 'disabled_course': course.is_disable }">
              {{ course.name }}
            </v-expansion-panel-header>
            <v-expansion-panel-content>
              ID: {{ course.id }}
              <v-divider></v-divider>
              LEVELS: {{ course.num_levels }}
              <v-divider></v-divider>
              WORDS: {{ course.num_things }}
              <v-divider></v-divider>
              DISABLE: {{ course.is_disable }}
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
          <template v-slot:item.level_number="{ item }">
            <a :href="item.host + item.course_url + item.level_number">{{ item.level_number }}</a>
          </template>
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
    </v-card>

    <v-card tile height="200" max-height="200" class="overflow-y-auto">
      <v-list dense>
        <v-subheader>Logs</v-subheader>
        <v-list-item
            v-for="(item, i) in notifications"
            :key="i"
            flat
        >
          <v-list-item-content>
            <v-list-item-title v-text="item" class="text_color"></v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
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
      ],
      // End Data tables params.
      // Begin Textarea
      singleLine: true,
      notifications: [],
      // End Textarea params.
    }
  },
  mounted() {
    this.getCourses();
    this.getWords();
  },
  created() {
    try {
      const socketHost = "ws://127.0.0.1:3000";
      const ws = new WebSocket(socketHost);

      ws.onmessage = ({data}) => {
        console.info(data);
        this.notifications.unshift((data + '\n'));
      }
    } catch (err) {
      console.log(err);
    }
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

<style>
.text_color {
  color: lime;
}

.disabled_course {
  color: #B71C1C;
}

.theme--dark.v-data-table > .v-data-table__wrapper > table > tbody > tr:hover:not(.v-data-table__expanded__content):not(.v-data-table__empty-wrapper){
  background: #78909C !important;
  color: black !important;
}
</style>