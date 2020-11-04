module.exports = {
    transpileDependencies: [
        "vuetify"
    ],
    assetsDir: 'vue-static/',
    devServer: {
        proxy: 'http://localhost:8000'
    }
}