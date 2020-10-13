<template>
  <v-container fluid>
    <v-card
        class="justify-space-around"
    >
      <v-card-title>
        Duplicates
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
          group-by="word_a"
          :loading-text="loadingText"
          height="860"
          show-group-by
      >
        <template v-slot:item.level_number="{ item }">
          <a :href="item.host + item.course_url + item.level_number">{{ item.level_number }}</a>
        </template>
      </v-data-table>

    </v-card>

  </v-container>
</template>


<script>
import axios from 'axios'
import Helpers from "@/helpers";

export default {
  name: "Duplicates",
  mixins: [Helpers],
  data: function () {
    return {
      words: [],
      overlay: false,
      // Begin Data tables params.
      search: '',
      loading: false,
      loadingText: 'Loading... Please wait',
      itemsPerPage: -1,
      headers: [
        {text: 'WORD A', value: 'word_a'},
        {text: 'WORD B', value: 'word_b'},
        {text: 'COURSE', value: 'course_name'},
        {text: 'LEVEL', value: 'level_number'},
      ],
      // End Data tables params.
    }
  },
  mounted() {
    this.getDuplicates();
  },
  methods: {
    getDuplicates: function () {
      const apiUrl = '/api/duplicates/';
      this.overlay = true;
      axios.get(apiUrl)
          .then((response) => {
            this.words = response.data;
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
    }
  }
}
</script>

<style scoped lang="scss">

</style>