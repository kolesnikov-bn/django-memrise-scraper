<template>
  <div class="container">
    <h1>List of Courses</h1>

    <ul id="v-for" class="demo">
      <li v-for="course in courses"
          :key="course.id"
          :title="course.name"
      >
        {{course.name}}
      </li>
    </ul>

  </div>
  <button class="btn btn-primary my-2 my-sm-0" v-on:click.prevent="updateCourses()">Update All Courses</button>
  <div class="loading" v-if="loading===true">Loading...</div>
</template>

<script>
import axios from 'axios'

export default {
  name: "Courses",
  data() {
    return {
      courses: [],
      loading: true,
      status: null,
      message: null,
    }
  },
  mounted() {
    this.getCourses();
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
          })
    },
    updateCourses: function () {
      const apiUrl = '/update';
      console.log('Pressed update key');
      // this.loading = true;
      // axios.get(apiUrl)
      //     .then((response) => {
      //       if (response.status === 200) {
      //         this.status = true;
      //       }
      //       this.loading = false
      //     })
    }
  }
}
</script>

<style scoped>

</style>