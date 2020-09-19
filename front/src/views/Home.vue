<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png">
    <Courses></Courses>
  </div>
</template>

<script lang="ts">
import {Options, Vue} from 'vue-class-component';
import Courses from "@/components/Courses.vue"; // @ is an alias to /src

@Options({
  components: {
    Courses,
  },
})
export default class Home extends Vue {
}
</script>
