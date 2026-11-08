
<script setup>
import { ref, watch, onMounted } from 'vue'

import { api } from './api'
import { LIMITE_ESTOQUE_BAIXO } from './constants'

import ProdutoForm from './components/ProdutoForm.vue'
import ProdutoTabela from './components/ProdutoTabela.vue'
import MovimentacaoForm from './components/MovimentacaoForm.vue'

const produtos = ref([])
const apenasBaixo = ref(false)
const carregando = ref(false)
const erro = ref('')
const movimento = ref(null)

async function carregar() {
  carregando.value = true
  erro.value = ''

  try {
    produtos.value = await api.listarProdutos(
      apenasBaixo.value ? LIMITE_ESTOQUE_BAIXO : null
    )
  } catch (e) {
    erro.value = e.message
  } finally {
    carregando.value = false
  }
}

function abrirMovimento({ produto, tipo }) {
  movimento.value = { produto, tipo }
}

function movimentoSalvo() {
  movimento.value = null
  carregar()
}

onMounted(carregar)

watch(apenasBaixo, carregar)
</script>

<template>
  <main>
    <h1>Controle de Estoque</h1>

    <ProdutoForm @criado="carregar" />

    <MovimentacaoForm
      v-if="movimento"
      :produto="movimento.produto"
      :tipo="movimento.tipo"
      @salvo="movimentoSalvo"
      @cancelar="movimento = null"
    />

    <section class="card">
      <div class="topo">
        <h2>Produtos</h2>

        <label>
          <input
            v-model="apenasBaixo"
            type="checkbox"
          />

          Só estoque baixo (≤ {{ LIMITE_ESTOQUE_BAIXO }})
        </label>
      </div>

      <p v-if="erro" class="erro">
        {{ erro }}
      </p>

      <p v-else-if="carregando">
        Carregando...
      </p>

      <p v-else-if="produtos.length === 0">
        Nenhum produto encontrado.
      </p>

      <ProdutoTabela
        v-else
        :produtos="produtos"
        @movimentar="abrirMovimento"
      />
    </section>
  </main>
</template>
