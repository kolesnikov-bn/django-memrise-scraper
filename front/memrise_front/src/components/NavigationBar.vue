<template>
  <v-navigation-drawer
      v-model="drawer"
      clipped
      fixed
      :color="color"
      :expand-on-hover="expandOnHover"
      :mini-variant="miniVariant"
      :permanent="permanent"
      dark
      app
  >
      <v-list
          dense
          nav
          class="py-0"
        >
          <v-list-item two-line :class="miniVariant && 'px-0'">
            <v-list-item-content>
              <v-list-item-title>Navigation</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-divider></v-divider>
          <v-list-item
            v-for="item in items"
            :key="item.title"
            link
          >
            <v-list-item-icon>
              <v-icon>{{ item.icon }}</v-icon>
            </v-list-item-icon>

            <v-list-item-content>
              <v-list-item-title>{{ item.title }}</v-list-item-title>
            </v-list-item-content>

          </v-list-item>
        </v-list>
  </v-navigation-drawer>
</template>

<script>
export default {
  name: "NavigationBar",
  data() {
    return {
      color: 'dark',
      drawer: true,
      permanent: false,
      miniVariant: true,
      expandOnHover: true,
      items: [
          { title: 'Dashboard', icon: 'mdi-view-dashboard' },
        ],
    }
  }
}
</script>

<style scoped>

</style>