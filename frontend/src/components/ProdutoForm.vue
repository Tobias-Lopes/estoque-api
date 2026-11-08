
<script setup>
import { ref } from 'vue'
import { api } from '../api'

const emit = defineEmits(['criado'])

const sku = ref('')
const nome = ref('')
const margem = ref(30)

const erro = ref('')
const enviando = ref(false)

async function enviar() {
  erro.value = ''
  enviando.value = true

  try {
    await api.criarProduto({
      sku: sku.value.trim(),
      nome: nome.value.trim(),
      margem_percentual: margem.value,
    })

    sku.value = ''
    nome.value = ''
    margem.value = 30

    emit('criado')
  } catch (e) {
    erro.value = e.message
  } finally {
    enviando.value = false
  }
}
</script>

<template>
  <form class="card" @submit.prevent="enviar">
    <h2>Novo produto</h2>

    <div class="linha">
      <input
        v-model="sku"
        placeholder="SKU"
        maxlength="40"
        required
      />

      <input
        v-model="nome"
        placeholder="Nome"
        maxlength="120"
        required
      />

      <label>
        Margem (%)
        <input
          v-model.number="margem"
          type="number"
          min="0"
          max="500"
          required
        />
      </label>

      <button :disabled="enviando">
        Cadastrar
      </button>
    </div>

    <p v-if="erro" class="erro">
      {{ erro }}
    </p>
  </form>
</template>
