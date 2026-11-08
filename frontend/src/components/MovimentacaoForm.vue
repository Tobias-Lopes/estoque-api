
<script setup>
import { ref, computed } from 'vue'
import { api } from '../api'
import { reaisParaCentavos } from '../format'

const props = defineProps({
  produto: {
    type: Object,
    required: true,
  },

  tipo: {
    type: String,
    required: true,
  },
})

const emit = defineEmits(['salvo', 'cancelar'])

const quantidade = ref(1)
const custo = ref('')
const erro = ref('')
const enviando = ref(false)

const ehCompra = computed(() => props.tipo === 'compra')

async function enviar() {
  erro.value = ''
  enviando.value = true

  try {
    if (ehCompra.value) {
      const centavos = reaisParaCentavos(custo.value)

      if (!(centavos > 0)) {
        throw new Error('Informe um custo unitário válido')
      }

      await api.registrarCompra(props.produto.id, {
        quantidade: quantidade.value,
        custo_unitario_centavos: centavos,
      })
    } else {
      await api.registrarSaida(props.produto.id, {
        quantidade: quantidade.value,
      })
    }

    emit('salvo')
  } catch (e) {
    erro.value = e.message
  } finally {
    enviando.value = false
  }
}
</script>

<template>
  <form class="card destaque" @submit.prevent="enviar">
    <h2>
      {{ ehCompra ? 'Registrar compra' : 'Registrar saída' }}:
      {{ produto.nome }}
    </h2>

    <div class="linha">
      <label>
        Quantidade
        <input
          v-model.number="quantidade"
          type="number"
          min="1"
          step="1"
          required
        />
      </label>

      <label v-if="ehCompra">
        Custo unitário (R$)
        <input
          v-model="custo"
          inputmode="decimal"
          placeholder="12,50"
          required
        />
      </label>

      <button :disabled="enviando">
        Confirmar
      </button>

      <button
        type="button"
        class="secundario"
        @click="emit('cancelar')"
      >
        Cancelar
      </button>
    </div>

    <p v-if="erro" class="erro">
      {{ erro }}
    </p>
  </form>
</template>
