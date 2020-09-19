<template>
  <v-app dark>
    <NavigationBar/>
    <Header/>
    <v-main>
      <Courses/>
    </v-main>
    <Footer/>
  </v-app>
</template>

<script>
import Courses from "@/components/Courses";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import NavigationBar from "@/components/NavigationBar";

export default {
  name: 'App',

  components: {
    Courses,
    Header,
    Footer,
    NavigationBar
  },

  data: () => ({
    //
  }),
};
</script>
