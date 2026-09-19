(() => {
  'use strict';

  // Translate presentation metadata only. Keep research Python files and raw outputs intact.
  const metadataEnglish = new Map([
    [
        "GPT-2 · Eğitim öncesi",
        "GPT-2 · Before fine-tuning"
    ],
    [
        "Özel bilgiler öğretilmeden önce",
        "Before the experimental facts were taught"
    ],
    [
        "800 adım; tekrar yöntemlerinden önce",
        "800 updates; before replay policies diverge"
    ],
    [
        "Yayımlanmış GPT-2 124M yapılandırması; yerel dosya yok",
        "Published GPT-2 124M configuration; no local file"
    ],
    [
        "Yerel model yapılandırması",
        "Local model configuration"
    ],
    [
        "Son yöntem modelleri kayıtlı değil. Canlı deneme başlangıç modeliyle yapılır; sağdaki kayıtlar son deneylere aittir.",
        "Final policy checkpoints were not saved. Live inference uses a base or common checkpoint; the records panel shows historical experiments."
    ],
    [
        "Kaydedilmiş deney ölçümleri; canlı model değil",
        "Saved experimental measurements, not the live model"
    ],
    [
        "Model dosya listesi geçersiz.",
        "Invalid model file list."
    ],
    [
        "Bilinmeyen model seçimi.",
        "Unknown model selection."
    ],
    [
        "Geçersiz model tohumu.",
        "Invalid model seed."
    ],
    [
        "Deneyde kullanılan model veya metin-parçalayıcı dosyası eksik.",
        "A model or tokenizer file used in the experiment is missing."
    ],
    [
        "Model veya metin-parçalayıcı dosyası deneydeki imzayla eşleşmiyor.",
        "A model or tokenizer file does not match its experimental checksum."
    ],
    [
        "Bu deney, tohum ve yöntem birlikte bulunmuyor.",
        "This study, seed and policy combination is unavailable."
    ],
    [
        "İstek bir JSON nesnesi olmalı.",
        "The request must be a JSON object."
    ],
    [
        "1–2000 karakter arasında, boş olmayan bir cümle yaz.",
        "Enter a non-empty prefix between 1 and 2,000 characters."
    ],
    [
        "Cevap uzunluğu 1–64 arasında tam sayı olmalı.",
        "Output length must be an integer between 1 and 64."
    ],
    [
        "Rastgelelik tohumu 0–2147483647 arasında tam sayı olmalı.",
        "Random seed must be an integer between 0 and 2147483647."
    ],
    [
        "Çeşitlilik geçerli bir sayı olmalı.",
        "Temperature must be a valid number."
    ],
    [
        "Çeşitlilik 0 veya 0,1–1,5 arasında olmalı.",
        "Temperature must be 0 or between 0.1 and 1.5."
    ],
    [
        "Model cevap üretiyor. Bitince belleği boşaltabilirsin.",
        "The model is generating. You can release its memory when it finishes."
    ],
    [
        "Bu model için gerekli yerel dosyalar bulunamadı. Playground README içindeki model kurulumunu kontrol et.",
        "Required local model files are missing. Check model setup in the playground README."
    ],
    [
        "Beklenen GPT-2 124M mimarisi bulunamadı.",
        "The expected GPT-2 124M architecture was not found."
    ],
    [
        "Model dosyası deney kaydındaki imzayla eşleşmiyor; güvenli biçimde durduruldu.",
        "The checkpoint does not match its experimental checksum. Loading was safely stopped."
    ],
    [
        "Başka bir cevap üretiliyor. Bitmesini bekleyip yeniden dene.",
        "Another response is being generated. Wait for it to finish and try again."
    ],
    [
        "Bu metin çok fazla parçaya ayrılıyor; daha kısa bir cümle dene (en çok 512 parça).",
        "This input has too many tokens. Try a shorter prefix (up to 512 tokens)."
    ],
    [
        "Bu HTTP işlemi desteklenmiyor veya istek biçimi geçersiz.",
        "This HTTP operation is unsupported or the request is malformed."
    ],
    [
        "Bu arayüz yalnızca kendi yerel adresinden kullanılabilir.",
        "This interface can only be used from its own local address."
    ],
    [
        "Böyle bir sayfa veya işlem yok.",
        "This page or operation does not exist."
    ],
    [
        "Seçilen kayıt veya istek geçersiz.",
        "The selected record or request is invalid."
    ],
    [
        "Gerekli yerel kayıt dosyası bulunamadı veya eksik.",
        "A required local record file is missing or incomplete."
    ],
    [
        "Oturum doğrulanamadı. Sayfayı yenileyip yeniden dene.",
        "Session verification failed. Refresh the page and try again."
    ],
    [
        "Böyle bir işlem yok. Eğitim veya kayıt değiştirme desteklenmiyor.",
        "This operation does not exist. Training and record editing are not supported."
    ],
    [
        "İstek boyutu geçersiz veya fazla büyük.",
        "The request size is invalid or too large."
    ],
    [
        "İstek JSON biçiminde olmalı.",
        "The request must use JSON format."
    ],
    [
        "Model çalıştırılamadı. Yerel model kurulumu veya bellek yetersiz olabilir; kayıtlara dokunulmadı.",
        "The model could not run. Check the local model installation and available memory. Records were not changed."
    ]
]);

  function englishMetadata(value) {
    if (typeof value !== 'string') return value;
    const checkpoint = /^Deney 13 · Başlangıç · Tohum (12|13|14)$/.exec(value);
    if (checkpoint) return `Study 13 · Common checkpoint · Seed ${checkpoint[1]}`;
    return metadataEnglish.get(value) ?? value;
  }

  const state = {
    token: null,
    bootstrap: null,
    selectedModel: null,
    modelUnloaded: false,
    isGenerating: false,
    isUnloading: false,
    turns: [],
    facts: [],
    factsRequest: 0,
    factsController: null,
    logsRequest: 0,
    logsController: null,
  };

  const $ = (id) => document.getElementById(id);
  const els = {
    architecturePanel: $('architecture-panel'),
    logsPanel: $('logs-panel'),
    architectureToggle: $('architecture-toggle'),
    logsToggle: $('logs-toggle'),
    connectionDot: $('connection-dot'),
    connectionLabel: $('connection-label'),
    bootstrapNotice: $('bootstrap-notice'),
    modelBadge: $('model-badge'),
    modelSelect: $('model-select'),
    modelStage: $('model-stage'),
    unloadButton: $('unload-button'),
    factSearch: $('fact-search'),
    factList: $('fact-list'),
    promptInput: $('prompt-input'),
    promptCount: $('prompt-count'),
    lengthInput: $('length-input'),
    temperatureInput: $('temperature-input'),
    seedInput: $('seed-input'),
    generateButton: $('generate-button'),
    generateLabel: $('generate-label'),
    generationStatus: $('generation-status'),
    clearChatButton: $('clear-chat-button'),
    conversation: $('conversation'),
    emptyConversation: $('empty-conversation'),
    transformerStack: $('transformer-stack'),
    blockCountLabel: $('block-count-label'),
    detailLabel: $('detail-label'),
    detailTitle: $('detail-title'),
    detailCopy: $('detail-copy'),
    specLayers: $('spec-layers'),
    specHeads: $('spec-heads'),
    specWidth: $('spec-width'),
    specVocab: $('spec-vocab'),
    specContext: $('spec-context'),
    architectureSource: $('architecture-source'),
    studySelect: $('study-select'),
    logSeedSelect: $('log-seed-select'),
    armSelect: $('arm-select'),
    logHistoryLabel: $('log-history-label'),
    logsStatus: $('logs-status'),
    logSummary: $('log-summary'),
    logTableWrap: $('log-table-wrap'),
    logTableBody: $('log-table-body'),
    rawLog: $('raw-log'),
  };

  const architectureCopy = {
    input: {
      label: 'Input',
      title: 'Text prefix',
      copy: 'The model sees only the English prefix in this attempt. Previous attempts and hidden chat history are not sent.',
    },
    token: {
      label: 'Tokenization',
      title: 'What is a token?',
      copy: 'A token is a small piece of text the model can read: a word, part of a word, or a piece that includes a space.',
    },
    embedding: {
      label: 'Representation',
      title: 'What is an embedding?',
      copy: 'An embedding turns a token into a vector of numbers. The model computes relationships using these numerical representations.',
    },
    transformer: {
      label: 'Processing',
      title: 'Transformer block',
      copy: 'Each block performs two main operations: attention combines relationships among earlier tokens, and feedforward transforms those features.',
    },
    attention: {
      label: 'Operation',
      title: 'Causal attention',
      copy: 'Attention weighs relationships with earlier tokens. The causal rule prevents it from looking at future tokens.',
    },
    feedforward: {
      label: 'Operation',
      title: 'Feedforward',
      copy: 'The feedforward layer transforms features at each position separately. This is not training: the model weights do not change.',
    },
    residual: {
      label: 'Operation',
      title: 'Normalization + residual skip',
      copy: 'Normalization balances the scale of values. A residual connection adds the new transformation to the previous representation.',
    },
    output: {
      label: 'Output',
      title: 'Next-token probabilities',
      copy: 'The model assigns probabilities across its vocabulary for the next token. This interface shows only the distribution for the first new token.',
    },
  };

  function setText(element, value) {
    element.textContent = value == null ? '' : String(value);
  }

  function setStatus(element, message, type = '') {
    element.className = type ? `status-message status-message--${type}` : 'status-message';
    setText(element, message);
  }

  function setConnection(connected, message) {
    els.connectionDot.classList.toggle('is-live', connected);
    els.connectionDot.classList.toggle('is-error', !connected);
    setText(els.connectionLabel, message);
  }

  function formatNumber(value, digits = 3) {
    const number = Number(value);
    if (!Number.isFinite(number)) return '—';
    return new Intl.NumberFormat('en-GB', { maximumFractionDigits: digits }).format(number);
  }

  function formatPercent(value) {
    const number = Number(value);
    if (!Number.isFinite(number)) return '—';
    return `${formatNumber(number * 100, 1)}%`;
  }

  function formatTime(value) {
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return 'unknown time';
    return new Intl.DateTimeFormat('en-GB', { dateStyle: 'short', timeStyle: 'short' }).format(date);
  }

  async function readResponse(response) {
    let payload = null;
    try {
      payload = await response.json();
    } catch (error) {
      throw new Error('The server did not return a readable response.');
    }
    if (!response.ok) {
      throw new Error(payload && payload.error ? englishMetadata(payload.error) : 'The request could not be completed.');
    }
    return payload;
  }

  async function fetchJson(url, options = {}) {
    const response = await fetch(url, options);
    return readResponse(response);
  }

  function apiHeaders(json = false) {
    const headers = {};
    if (state.token) headers['X-SpacingLab-Token'] = state.token;
    if (json) headers['Content-Type'] = 'application/json';
    return headers;
  }

  function modelById(id) {
    return (state.bootstrap?.models || []).find((model) => model.id === id) || null;
  }

  function modelLabel(model) {
    if (!model) return 'No model';
    return englishMetadata(model.label) || model.id;
  }

  function renderArchitecture(architecture = {}) {
    const layers = Number(architecture.layers) || 12;
    setText(els.blockCountLabel, `${layers} blocks`);
    setText(els.specLayers, formatNumber(architecture.layers ?? 12, 0));
    setText(els.specHeads, formatNumber(architecture.heads ?? 12, 0));
    setText(els.specWidth, formatNumber(architecture.width ?? 768, 0));
    setText(els.specVocab, formatNumber(architecture.vocab ?? 50257, 0));
    setText(els.specContext, formatNumber(architecture.context ?? 1024, 0));
    els.transformerStack.replaceChildren();

    for (let index = 1; index <= layers; index += 1) {
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'transformer-block';
      button.dataset.detail = 'transformer';
      button.setAttribute('aria-label', `Transformer block ${index}`);
      const number = document.createElement('span');
      number.className = 'block-number';
      setText(number, String(index).padStart(2, '0'));
      const title = document.createElement('span');
      title.className = 'block-title';
      setText(title, `Block ${index}`);
      const mark = document.createElement('span');
      mark.className = 'block-mark';
      mark.setAttribute('aria-hidden', 'true');
      setText(mark, '↗');
      button.append(number, title, mark);
      button.addEventListener('click', () => showArchitectureDetail('transformer'));
      els.transformerStack.append(button);
    }
  }

  function showArchitectureDetail(key) {
    const detail = architectureCopy[key] || architectureCopy.transformer;
    setText(els.detailLabel, detail.label);
    setText(els.detailTitle, detail.title);
    setText(els.detailCopy, detail.copy);
    document.querySelectorAll('[data-detail]').forEach((node) => {
      node.classList.toggle('is-selected', node.dataset.detail === key);
    });
  }

  function renderModels(models) {
    els.modelSelect.replaceChildren();
    models.forEach((model) => {
      const option = document.createElement('option');
      option.value = model.id;
      setText(option, model.available ? modelLabel(model) : `${modelLabel(model)} · weights unavailable`);
      option.disabled = !model.available;
      els.modelSelect.append(option);
    });

    const defaultModel = models.find((model) => model.id === 'study13-seed12-common' && model.available)
      || models.find((model) => model.available)
      || models[0];
    if (defaultModel) {
      els.modelSelect.value = defaultModel.id;
      selectModel(defaultModel.id);
    }
    els.modelSelect.disabled = models.length === 0;
  }

  function selectModel(id) {
    const model = modelById(id);
    state.selectedModel = model;
    state.modelUnloaded = false;
    setText(els.unloadButton, 'Unload model');
    if (!model) {
      setText(els.modelBadge, 'No model');
      setText(els.modelStage, 'Model not found.');
      updateControls();
      return;
    }
    setText(els.modelBadge, modelLabel(model));
    setText(els.modelStage, model.available ? `Stage: ${englishMetadata(model.stage) || 'unspecified'}` : 'No saved model weights are available for this selection.');
    loadFacts(model.id);
    updateControls();
  }

  function updateControls() {
    const modelAvailable = Boolean(state.selectedModel?.available);
    const ready = Boolean(state.bootstrap && modelAvailable && !state.isGenerating && !state.isUnloading);
    [els.promptInput, els.lengthInput, els.temperatureInput, els.seedInput].forEach((element) => {
      element.disabled = !state.bootstrap;
    });
    els.factSearch.disabled = !state.bootstrap;
    els.generateButton.disabled = !ready;
    els.unloadButton.disabled = !modelAvailable || state.modelUnloaded || state.isGenerating || state.isUnloading;
    els.clearChatButton.disabled = state.turns.length === 0;
    els.generateButton.classList.toggle('is-loading', state.isGenerating);
    els.unloadButton.classList.toggle('is-loading', state.isUnloading);
  }

  function renderFacts() {
    const query = els.factSearch.value.trim().toLocaleLowerCase('en-GB');
    const facts = state.facts.filter((fact) => {
      const haystack = `${fact.prompt || ''} ${fact.text || ''} ${fact.answer || ''}`.toLocaleLowerCase('en-GB');
      return haystack.includes(query);
    });
    els.factList.replaceChildren();
    if (!state.selectedModel?.available) {
      const empty = document.createElement('p');
      empty.className = 'empty-state';
      setText(empty, 'No saved model weights are available for this model.');
      els.factList.append(empty);
      return;
    }
    if (!facts.length) {
      const empty = document.createElement('p');
      empty.className = 'empty-state';
      setText(empty, state.facts.length ? 'No prefixes match this search.' : 'No learned facts are available to search for this model.');
      els.factList.append(empty);
      return;
    }
    facts.forEach((fact) => {
      const item = document.createElement('article');
      item.className = 'fact-item';
      const prompt = document.createElement('p');
      prompt.className = 'fact-prompt';
      setText(prompt, fact.prompt || fact.text || 'No text prefix');
      const choose = document.createElement('button');
      choose.type = 'button';
      choose.className = 'fact-select';
      setText(choose, 'Use prefix');
      choose.addEventListener('click', () => {
        els.promptInput.value = fact.prompt || fact.text || '';
        updatePromptCount();
        els.promptInput.focus();
        setStatus(els.generationStatus, 'Prefix inserted. Nothing has been generated yet.', 'info');
      });
      item.append(prompt, choose);

      if (fact.answer) {
        const answerDetails = document.createElement('details');
        answerDetails.className = 'fact-answer';
        const summary = document.createElement('summary');
        setText(summary, 'Reveal expected answer');
        const answer = document.createElement('p');
        setText(answer, fact.answer);
        answerDetails.append(summary, answer);
        item.append(answerDetails);
      }
      els.factList.append(item);
    });
  }

  async function loadFacts(modelId) {
    if (state.factsController) state.factsController.abort();
    const requestId = ++state.factsRequest;
    state.facts = [];
    renderFacts();
    state.factsController = new AbortController();
    try {
      const payload = await fetchJson(`/api/facts?model=${encodeURIComponent(modelId)}`, { signal: state.factsController.signal });
      if (requestId !== state.factsRequest) return;
      state.facts = Array.isArray(payload.facts) ? payload.facts : [];
      renderFacts();
    } catch (error) {
      if (error.name === 'AbortError' || requestId !== state.factsRequest) return;
      const empty = document.createElement('p');
      empty.className = 'empty-state empty-state--error';
      setText(empty, error.message);
      els.factList.replaceChildren(empty);
    }
  }

  function updatePromptCount() {
    const length = els.promptInput.value.length;
    setText(els.promptCount, `${formatNumber(length, 0)} / 2,000`);
    els.promptCount.classList.toggle('is-limit', length >= 2000);
  }

  function readSetting(element, label, { min, max, integer = false, step = null, temperature = false }) {
    const raw = element.value.trim();
    if (!raw) throw new Error(`${label} cannot be empty.`);
    const value = Number(raw);
    if (!Number.isFinite(value)) throw new Error(`${label} must be a number.`);
    if (integer && !Number.isInteger(value)) throw new Error(`${label} must be an integer.`);
    if (value < min || value > max) throw new Error(`${label} must be between ${min} and ${max}.`);
    if (step !== null && Math.abs(value / step - Math.round(value / step)) > 1e-9) {
      throw new Error(`${label} must use increments of ${step}.`);
    }
    if (temperature && value !== 0 && value < 0.1) {
      throw new Error('Sampling / temperature must be 0 or between 0.1 and 1.5.');
    }
    return value;
  }

  function renderConversation() {
    els.conversation.replaceChildren();
    if (!state.turns.length) {
      els.conversation.append(els.emptyConversation);
      updateControls();
      return;
    }
    state.turns.forEach((turn) => {
      const article = document.createElement('article');
      article.className = 'turn';
      const promptWrap = document.createElement('div');
      promptWrap.className = 'message message--prompt';
      const promptLabel = document.createElement('span');
      promptLabel.className = 'message-label';
      setText(promptLabel, 'Input');
      const prompt = document.createElement('p');
      prompt.className = 'message-text message-text--prompt';
      setText(prompt, turn.prompt);
      promptWrap.append(promptLabel, prompt);

      const completionWrap = document.createElement('div');
      completionWrap.className = 'message message--completion';
      const completionLabel = document.createElement('span');
      completionLabel.className = 'message-label';
      setText(completionLabel, 'GPT-2 continuation');
      const completion = document.createElement('p');
      completion.className = 'message-text';
      setText(completion, turn.completion || '(empty continuation)');
      const meta = document.createElement('p');
      meta.className = 'message-meta';
      setText(meta, `${turn.modelLabel || turn.model} · ${turn.stage || 'stage unspecified'} · ${formatTime(turn.time)} · ${formatNumber(turn.elapsedSeconds, 2)} s`);
      completionWrap.append(completionLabel, completion, meta);
      article.append(promptWrap, completionWrap);

      const inspect = document.createElement('details');
      inspect.className = 'turn-inspection';
      const inspectSummary = document.createElement('summary');
      setText(inspectSummary, 'Inspect tokens and first-token probabilities');
      const inspectionBody = document.createElement('div');
      inspectionBody.className = 'inspection-body';
      const settingsTitle = document.createElement('h3');
      setText(settingsTitle, 'Settings for this generation');
      const settings = turn.settings || {};
      const settingsReceipt = document.createElement('p');
      settingsReceipt.className = 'inspection-receipt';
      setText(settingsReceipt, `Output length ${formatNumber(settings.max_new_tokens, 0)} · temperature ${formatNumber(settings.temperature, 1)} · seed ${formatNumber(settings.seed, 0)} · device ${turn.device || 'unspecified'}`);
      const tokenTitle = document.createElement('h3');
      setText(tokenTitle, turn.inputFormat === 'plain'
        ? 'Input tokens · no special prefix added'
        : 'Input tokens · input format not recorded');
      const tokenList = document.createElement('div');
      tokenList.className = 'token-list';
      (turn.tokens || []).forEach((token) => {
        const chip = document.createElement('span');
        chip.className = 'token-chip';
        chip.title = `Token: ${token}`;
        setText(chip, token);
        tokenList.append(chip);
      });
      if (!tokenList.children.length) setText(tokenList, 'No token information returned.');
      const topTitle = document.createElement('h3');
      setText(topTitle, 'First next-token probabilities');
      const topList = document.createElement('div');
      topList.className = 'top-token-list';
      (turn.topTokens || []).forEach((token) => {
        const row = document.createElement('div');
        row.className = 'top-token-row';
        const tokenText = document.createElement('span');
        setText(tokenText, token.text);
        const probability = document.createElement('span');
        setText(probability, formatPercent(token.probability));
        row.append(tokenText, probability);
        topList.append(row);
      });
      if (!topList.children.length) setText(topList, 'No probability distribution returned.');
      const topNote = document.createElement('p');
      topNote.className = 'inspection-note';
      setText(topNote, 'These probabilities are measured before temperature sampling. They do not establish that the answer is correct.');
      inspectionBody.append(settingsTitle, settingsReceipt, tokenTitle, tokenList, topTitle, topNote, topList);
      inspect.append(inspectSummary, inspectionBody);
      article.append(inspect);
      els.conversation.append(article);
    });
    updateControls();
  }

  function setGenerationBusy(busy) {
    state.isGenerating = busy;
    setText(els.generateLabel, busy ? 'Model running…' : 'Generate continuation');
    updateControls();
  }

  async function generate() {
    if (state.isGenerating || state.isUnloading || !state.selectedModel?.available) return;
    const prompt = els.promptInput.value;
    if (!prompt.trim()) {
      setStatus(els.generationStatus, 'First write an English prefix to complete.', 'error');
      els.promptInput.focus();
      return;
    }
    let settings;
    try {
      settings = {
        max_new_tokens: readSetting(els.lengthInput, 'Output length', { min: 1, max: 64, integer: true, step: 1 }),
        temperature: readSetting(els.temperatureInput, 'Sampling / temperature', { min: 0, max: 1.5, step: 0.1, temperature: true }),
        seed: readSetting(els.seedInput, 'Random seed', { min: 0, max: 2147483647, integer: true, step: 1 }),
      };
    } catch (error) {
      setStatus(els.generationStatus, error.message, 'error');
      return;
    }
    const payload = { model: state.selectedModel.id, prompt, ...settings };
    setGenerationBusy(true);
    setStatus(els.generationStatus, 'Model running. The time depends on your device and selected checkpoint.', 'info');
    try {
      const response = await fetchJson('/api/generate', {
        method: 'POST',
        headers: apiHeaders(true),
        body: JSON.stringify(payload),
      });
      const turn = {
        prompt: response.prompt ?? prompt,
        completion: response.completion ?? '',
        model: response.model ?? payload.model,
        modelLabel: englishMetadata(response.model_label) ?? modelLabel(state.selectedModel),
        stage: englishMetadata(response.stage ?? state.selectedModel.stage),
        settings: response.settings ?? payload,
        time: new Date().toISOString(),
        elapsedSeconds: response.elapsed_seconds,
        device: response.device,
        checkpointVerified: response.checkpoint_verified,
        inputFormat: response.input_format,
        tokens: Array.isArray(response.tokens) ? response.tokens : [],
        topTokens: Array.isArray(response.top_tokens) ? response.top_tokens : [],
      };
      state.turns.push(turn);
      renderConversation();
      let verification = '';
      if (response.checkpoint_verified === true) {
        verification = ' Experimental checkpoint verified.';
      } else if (response.checkpoint_verified === false && response.model === 'gpt2-base') {
        verification = ' This is the base model, before the experimental facts were taught.';
      }
      if (response.model_files_verified === true) verification += ' Model files verified.';
      setStatus(els.generationStatus, `Completed.${verification}`, response.checkpoint_verified === true || response.model_files_verified === true ? 'success' : 'info');
    } catch (error) {
      setStatus(els.generationStatus, error.message, 'error');
    } finally {
      setGenerationBusy(false);
    }
  }

  async function unloadModel() {
    if (state.isGenerating || state.isUnloading || !state.token || !state.selectedModel?.available) return;
    state.isUnloading = true;
    setText(els.unloadButton, 'Unloading model…');
    setStatus(els.generationStatus, 'Releasing model memory.', 'info');
    updateControls();
    try {
      const response = await fetchJson('/api/unload', {
        method: 'POST',
        headers: apiHeaders(true),
        body: JSON.stringify({}),
      });
      if (response.unloaded === true) {
        state.modelUnloaded = true;
        setText(els.unloadButton, 'Model unloaded');
        setStatus(els.generationStatus, 'Model memory released. A new generation request can reload it.', 'success');
      } else {
        setText(els.unloadButton, 'Unload model');
        setStatus(els.generationStatus, 'Could not confirm that the model was unloaded.', 'error');
      }
    } catch (error) {
      setText(els.unloadButton, 'Unload model');
      setStatus(els.generationStatus, error.message, 'error');
    } finally {
      state.isUnloading = false;
      updateControls();
    }
  }

  function logControlsValue() {
    return {
      study: Number(els.studySelect.value),
      seed: Number(els.logSeedSelect.value),
      arm: els.armSelect.value,
    };
  }

  function armLabel(arm) {
    return arm === 'prioritized' ? 'Forgetting-prioritized' : 'Uniform random';
  }

  function updateSeedOptions() {
    const study = Number(els.studySelect.value);
    const seeds = study === 12 ? [9, 10, 11] : [12, 13, 14];
    const current = Number(els.logSeedSelect.value);
    els.logSeedSelect.replaceChildren();
    seeds.forEach((seed) => {
      const option = document.createElement('option');
      option.value = String(seed);
      setText(option, String(seed));
      els.logSeedSelect.append(option);
    });
    els.logSeedSelect.value = seeds.includes(current) ? String(current) : String(seeds[0]);
  }

  function renderLogSummary(summary) {
    els.logSummary.replaceChildren();
    if (!summary || typeof summary !== 'object' || Array.isArray(summary)) return;
    const simpleFields = [
      ['complete_pairs', 'Completed pairs'],
      ['complete_continuations', 'Completed continuations'],
    ];
    simpleFields.forEach(([key, labelText]) => {
      if (!(key in summary) || typeof summary[key] === 'object') return;
      const item = document.createElement('div');
      item.className = 'summary-item';
      const label = document.createElement('span');
      label.className = 'summary-label';
      setText(label, labelText);
      const valueText = document.createElement('strong');
      setText(valueText, formatNumber(summary[key], 0));
      item.append(label, valueText);
      els.logSummary.append(item);
    });
    const caution = document.createElement('p');
    caution.className = 'summary-caution';
    setText(caution, 'This summary shows completed record counts only. See the raw JSON for details.');
    els.logSummary.append(caution);
  }

  function renderLogs(payload, selection) {
    setText(els.logHistoryLabel, `Study ${selection.study} · seed ${selection.seed} · ${armLabel(selection.arm)} · historical record`);
    els.logTableBody.replaceChildren();
    const evals = Array.isArray(payload.evals) ? payload.evals : [];
    els.logTableWrap.hidden = !evals.length;
    if (evals.length) {
      evals.forEach((evaluation) => {
        const row = document.createElement('tr');
        [evaluation.int_step, formatPercent(evaluation.acc), formatNumber(evaluation.nll, 4), formatNumber(evaluation.disc, 4)].forEach((value) => {
          const cell = document.createElement('td');
          setText(cell, value);
          row.append(cell);
        });
        els.logTableBody.append(row);
      });
    }
    renderLogSummary(payload.summary);
    setText(els.rawLog, JSON.stringify(payload.raw ?? payload, null, 2));
  }

  async function loadLogs() {
    if (state.logsController) state.logsController.abort();
    const requestId = ++state.logsRequest;
    const selection = logControlsValue();
    setText(els.logHistoryLabel, `Study ${selection.study} · seed ${selection.seed} · ${armLabel(selection.arm)} · loading`);
    setStatus(els.logsStatus, 'Reading historical records.', 'info');
    els.logTableWrap.hidden = true;
    els.logSummary.replaceChildren();
    els.rawLog.textContent = 'Waiting for records.';
    state.logsController = new AbortController();
    const query = new URLSearchParams({ study: String(selection.study), seed: String(selection.seed), arm: selection.arm });
    try {
      const payload = await fetchJson(`/api/logs?${query.toString()}`, { signal: state.logsController.signal });
      if (requestId !== state.logsRequest) return;
      renderLogs(payload, selection);
      const hasEvals = Array.isArray(payload.evals) && payload.evals.length > 0;
      setStatus(els.logsStatus, hasEvals ? 'Records loaded.' : 'No evaluation rows for this selection.', hasEvals ? 'success' : 'info');
    } catch (error) {
      if (error.name === 'AbortError' || requestId !== state.logsRequest) return;
      els.logTableWrap.hidden = true;
      setStatus(els.logsStatus, error.message, 'error');
      setText(els.rawLog, 'Could not read records.');
    }
  }

  function togglePanel(panel, toggle, open) {
    panel.classList.toggle('is-open', open);
    panel.classList.toggle('is-collapsed', !open);
    toggle.setAttribute('aria-expanded', String(open));
    const workspace = document.querySelector('.workspace');
    workspace.classList.toggle('architecture-collapsed', els.architecturePanel.classList.contains('is-collapsed'));
    workspace.classList.toggle('logs-collapsed', els.logsPanel.classList.contains('is-collapsed'));
  }

  function initializePanels() {
    const mobile = window.matchMedia('(max-width: 940px)').matches;
    togglePanel(els.architecturePanel, els.architectureToggle, !mobile);
    togglePanel(els.logsPanel, els.logsToggle, !mobile);
  }

  function bindEvents() {
    els.modelSelect.addEventListener('change', () => selectModel(els.modelSelect.value));
    els.factSearch.addEventListener('input', renderFacts);
    els.promptInput.addEventListener('input', updatePromptCount);
    els.generateButton.addEventListener('click', generate);
    els.unloadButton.addEventListener('click', unloadModel);
    els.clearChatButton.addEventListener('click', () => {
      state.turns = [];
      renderConversation();
      setStatus(els.generationStatus, 'Visible history cleared. The server does not store it.', 'info');
    });
    els.studySelect.addEventListener('change', () => {
      updateSeedOptions();
      loadLogs();
    });
    els.logSeedSelect.addEventListener('change', loadLogs);
    els.armSelect.addEventListener('change', loadLogs);
    els.architectureToggle.addEventListener('click', () => {
      const open = !els.architecturePanel.classList.contains('is-open');
      togglePanel(els.architecturePanel, els.architectureToggle, open);
    });
    els.logsToggle.addEventListener('click', () => {
      const open = !els.logsPanel.classList.contains('is-open');
      togglePanel(els.logsPanel, els.logsToggle, open);
    });
    document.querySelectorAll('[data-close-panel]').forEach((button) => {
      button.addEventListener('click', () => {
        const panel = $(button.dataset.closePanel);
        const toggle = panel === els.architecturePanel ? els.architectureToggle : els.logsToggle;
        togglePanel(panel, toggle, false);
      });
    });
    document.querySelectorAll('[data-detail]').forEach((node) => {
      node.addEventListener('click', () => showArchitectureDetail(node.dataset.detail));
    });
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape') {
        togglePanel(els.architecturePanel, els.architectureToggle, false);
        togglePanel(els.logsPanel, els.logsToggle, false);
      }
    });
  }

  async function bootstrap() {
    bindEvents();
    initializePanels();
    renderArchitecture();
    showArchitectureDetail('transformer');
    updatePromptCount();
    renderConversation();
    updateSeedOptions();
    loadLogs();
    try {
      const payload = await fetchJson('/api/bootstrap');
      state.bootstrap = payload;
      state.token = payload.token || null;
      renderArchitecture(payload.architecture || {});
      showArchitectureDetail('transformer');
      renderModels(Array.isArray(payload.models) ? payload.models : []);
      setConnection(true, 'Local connection ready');
      setText(els.architectureSource, englishMetadata(payload.architecture_source) || 'Architecture source unspecified.');
      if (payload.notice) {
        els.bootstrapNotice.hidden = false;
        setText(els.bootstrapNotice, englishMetadata(payload.notice));
      }
    } catch (error) {
      setConnection(false, 'Local connection failed');
      setText(els.modelBadge, 'Connection failed');
      els.bootstrapNotice.hidden = false;
      setText(els.bootstrapNotice, error.message);
      setStatus(els.generationStatus, 'Could not load model information. Refresh the page when the local server is ready.', 'error');
    } finally {
      updateControls();
    }
  }

  bootstrap();
})();
