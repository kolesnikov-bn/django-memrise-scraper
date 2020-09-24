/**
* Модуль для хранения глобальных переменных для работы приложения
* */

/* Константы */
const BaseURL = getBaseURL();


/* Вспомогательные функции */
/**
 * Получаем по переменной окружения адрес web интерфейса
 * Если получен development, то задаем собственный локальный адрес
 * Если установлен другой режим, тогда работаем с глобальным адресом контейнера
 *
 * @return {string}: адрес работы интерфейса
 * */
function getBaseURL() {
  let mode = process.env.NODE_ENV;
  if (mode === 'development'){
    return 'http://localhost:8081/'
  } else {
    return '/vue-static/'
  }
}

export default {
  BaseURL
}
