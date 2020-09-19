<template>
  <v-app-bar
      dark
      app
  >
    <v-toolbar-title>Memrise Web Scraper</v-toolbar-title>

    <v-spacer></v-spacer>

    <v-btn icon>
      <v-icon>mdi-magnify</v-icon>
    </v-btn>

    <v-menu
        left
        bottom
    >
    </v-menu>
  </v-app-bar>


</template>

<script>
export default {
  name: "Header"
}
</script>

<style scoped>

</style>