/**
 * File Name: friction.js
 * Role: Member 4 - Adaptation Engine & AI Connection Module
 */

class AdaptiEngine {
  constructor(config = {}) {
    this.frictionScore = 0;
    this.threshold = config.threshold || 50;
    this.decayRate = config.decayRate || 5;
    this.decayIntervalMs = config.decayIntervalMs || 10000;
    
    this.activeAdaptations = new Set();
    this.listeners = [];

    // Automatically decay score over time so old friction fades
    this.startDecaySystem();
  }

  /**
   * Add friction points and evaluate threshold state
   */
  addFriction(points, reason) {
    this.frictionScore += points;
    console.log(`[ADAPTI] ⚠️ ${reason}: +${points} | Current Score: ${this.frictionScore}`);
    this.evaluate();
    this.notify();
  }

  /**
   * Reset friction state back to default
   */
  resetScore() {
    this.frictionScore = 0;
    this.activeAdaptations.clear();
    console.log("[ADAPTI] Friction score reset.");
    this.evaluate();
    this.notify();
  }

  /**
   * Periodically reduce friction score over time
   */
  startDecaySystem() {
    setInterval(() => {
      if (this.frictionScore > 0) {
        this.frictionScore = Math.max(0, this.frictionScore - this.decayRate);
        console.log(`[ADAPTI] ⏳ Friction decayed. Current Score: ${this.frictionScore}`);
        this.evaluate();
        this.notify();
      }
    }, this.decayIntervalMs);
  }

  /**
   * Evaluate friction score against active threshold rules
   */
  evaluate() {
    if (this.frictionScore >= this.threshold) {
      if (!this.activeAdaptations.has("SIMPLIFY_MODE")) {
        this.activeAdaptations.add("SIMPLIFY_MODE");
        this.triggerAdaptation("SIMPLIFY_MODE", {
          biggerButtons: true,
          lessClutter: true,
          simplifiedText: true,
          stepByStep: true,
        });
      }
    } else {
      if (this.activeAdaptations.has("SIMPLIFY_MODE")) {
        this.activeAdaptations.delete("SIMPLIFY_MODE");
        this.triggerAdaptation("NORMAL_MODE", {
          biggerButtons: false,
          lessClutter: false,
          simplifiedText: false,
          stepByStep: false,
        });
      }
    }
  }

  /**
   * Core action emitter for UI integrations
   */
  triggerAdaptation(mode, config) {
    console.log(`\n========================================`);
    console.log(`🚀 [ADAPTI ACTION] Triggering: ${mode}`);
    console.log(`Config:`, config);
    console.log(`========================================\n`);
  }

  /**
   * Send natural language text to AI endpoint (http://127.0.0.1:8000/adapt)
   */
  async analyzeWithAI(userText) {
    try {
      console.log(`[ADAPTI AI] Sending text to /adapt: "${userText}"`);

      const response = await fetch("http://127.0.0.1:8000/adapt", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: userText, user_input: userText })
      });

      if (!response.ok) {
        throw new Error(`AI HTTP Error: ${response.status}`);
      }

      const data = await response.json();
      console.log("[ADAPTI AI] Response received:", data);

      const action = data?.adaptation?.action || data?.action;
      if (action) {
        this.handleAIAction(action, data);
      }
    } catch (error) {
      console.warn("[ADAPTI AI] Backend connection issue. Running local fallback analysis...", error);
      
      // Local fallback parser so your UI demo never breaks
      const cleanText = userText.toLowerCase();
      let fallbackAction = "default";

      if (cleanText.includes("small") || cleanText.includes("read") || cleanText.includes("font") || cleanText.includes("bigger")) {
        fallbackAction = "increase_font_size";
      } else if (cleanText.includes("simplify") || cleanText.includes("hard") || cleanText.includes("clutter")) {
        fallbackAction = "simplify_mode";
      }

      this.handleAIAction(fallbackAction, { fallback: true });
    }
  }
  /**
   * Process decision returned from the AI endpoint
   */
  handleAIAction(action, rawData) {
    console.log(`\n🤖 [AI DECISION RECEIVED]: ${action}`);

    switch (action) {
      case "increase_font_size":
        this.triggerAdaptation("INCREASE_FONT_SIZE", { fontSizeMultiplier: 1.25 });
        break;

      case "simplify_mode":
      case "enable_simplify":
        this.addFriction(50, "AI Explicit Simplify Trigger");
        break;

      case "start_guided_mode":
        this.triggerAdaptation("GUIDED_MODE", { active: true });
        break;

      default:
        console.log(`[ADAPTI AI] Logged action: ${action}`, rawData);
        break;
    }
  }

  // Common Manual Friction Triggers
  repeatedClick() { this.addFriction(15, "Repeated Click"); }
  formError() { this.addFriction(20, "Form Validation Error"); }
  backtracking() { this.addFriction(20, "Rapid Backtracking"); }
  longInactivity() { this.addFriction(10, "Long Inactivity"); }

  /**
   * Listener system for UI integration
   */
  subscribe(callback) {
    this.listeners.push(callback);
  }

  notify() {
    const state = {
      score: this.frictionScore,
      isHighFriction: this.frictionScore >= this.threshold,
      adaptations: Array.from(this.activeAdaptations),
    };
    this.listeners.forEach((fn) => fn(state));
  }
}

// Module export for Node.js test runs or browser environment
if (typeof module !== "undefined" && module.exports) {
  module.exports = AdaptiEngine;
} else {
  window.AdaptiEngine = AdaptiEngine;
}