<template>
  <v-card>
    <v-app-bar app prominent>
      <v-app-bar-nav-icon @click="drawer = true"></v-app-bar-nav-icon>

      <v-toolbar-title>
        <router-link to="/" class="route-home">Memrise Web Scraper</router-link>
      </v-toolbar-title>

      <v-navigation-drawer
          v-model="drawer"
          absolute
          clipped
          temporary
      >
        <v-list
            nav
            dense
        >
          <v-list-item-group
              v-model="group"
              active-class="orange--text text--accent-4"
          >
            <v-list-item to="/">
              <v-list-item-icon>
                <v-icon>mdi-home</v-icon>
              </v-list-item-icon>
              <v-list-item-title>Home</v-list-item-title>
            </v-list-item>

            <v-list-item to="/duplicates">
              <v-list-item-icon>
                <v-icon>mdi-account</v-icon>
              </v-list-item-icon>
              <v-list-item-title>Duplicates</v-list-item-title>
            </v-list-item>
          </v-list-item-group>
        </v-list>
      </v-navigation-drawer>


    </v-app-bar>

  </v-card>



</template>

<script>
export default {
  name: "Header",
  data: () => ({
    drawer: false,
    group: null,
  }),
}
</script>

<style lang="scss" scoped>
  .header-container {
    margin-bottom: 200px;
  }

  .route-home{
    color: #ffffff;
    text-decoration: none;

    &:visited {
      color: #ffffff;
      text-decoration: none;
     }
    &:hover {
      color: #a9b5c1;
    }
  }

</style>