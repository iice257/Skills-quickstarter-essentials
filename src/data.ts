import {
  Blocks,
  Bot,
  Box,
  Braces,
  Brush,
  Bug,
  CheckCircle2,
  FileText,
  FlaskConical,
  Gem,
  GitPullRequest,
  Globe2,
  Layers3,
  Lightbulb,
  MonitorSmartphone,
  PackageCheck,
  Rocket,
  ShieldCheck,
  Sparkles,
  Star,
  TerminalSquare,
  TestTube2,
  WandSparkles,
  Workflow
} from "lucide-react";
import type { LucideIcon } from "lucide-react";

export const repoUrl = "https://github.com/iice257/Skills-quickstarter";
export const commandRepoBase = "https://github.com/iice257/Skills";
export const githubProfileUrl = "https://github.com/iice257";
export const xProfileUrl = "https://x.com/iice257";

const installCommand = (path: string) => `$skill-starter install ${commandRepoBase}/${path}`;

export type NavItem = {
  label: string;
  href: string;
  section: SectionKey;
};

export type SectionKey = "home" | "categories" | "scenarios" | "providers" | "favorites" | "about";

export const navItems: NavItem[] = [
  { label: "Home", href: "#home", section: "home" },
  { label: "Categories", href: "#categories", section: "categories" },
  { label: "Scenarios", href: "#scenarios", section: "scenarios" },
  { label: "Providers", href: "#providers", section: "providers" },
  { label: "Favorites", href: "#favorites", section: "favorites" },
  { label: "About", href: "#about", section: "about" }
];

export type CommandRow = {
  label: string;
  description: string;
  command: string;
  icon: LucideIcon;
};

export const commands: CommandRow[] = [
  {
    label: "Guided setup",
    description: "Starts from the README so the agent asks what you need.",
    command: `$skill-starter install ${commandRepoBase}/readme.md`,
    icon: Sparkles
  },
  {
    label: "Lightweight quickstart",
    description: "Small starter setup without installing everything.",
    command: `$skill-starter install ${commandRepoBase}/tree/main/categories/lightweight-quickstart`,
    icon: PackageCheck
  },
  {
    label: "Web development setup",
    description: "Frontend, design, browser testing, CI, and deployment.",
    command: `$skill-starter install ${commandRepoBase}/tree/main/categories/web-development-setup`,
    icon: Globe2
  },
  {
    label: "Full startup",
    description: "Installs the full skill catalog.",
    command: `$skill-starter install ${commandRepoBase}/tree/main/categories/full-startup`,
    icon: Blocks
  },
  {
    label: "Favourites",
    description: "Installs the current capped shortlist.",
    command: `$skill-starter install ${commandRepoBase}/tree/main/favourites`,
    icon: CheckCircle2
  }
];

export const needCards = [
  {
    title: "Categories",
    text: "Install paths grouped by the kind of work you do.",
    href: `${repoUrl}/tree/main/categories`,
    action: "Browse categories",
    icon: Layers3,
    command: installCommand("tree/main/categories"),
    summary: "Installs from the category index so your agent can pick focused work bundles.",
    includes: ["Scenario folders", "Provider packs", "Focused setup paths"]
  },
  {
    title: "Scenarios",
    text: "Use-case bundles for different setups.",
    href: "#scenarios",
    action: "View bundles",
    icon: Workflow,
    command: installCommand("tree/main/categories/web-development-setup"),
    summary: "Starts with practical setup bundles grouped by workflow.",
    includes: ["Web development setup", "Debugging", "Deployment"]
  },
  {
    title: "Favourites",
    text: "The capped shortlist for a fast high-value setup.",
    href: `${repoUrl}/tree/main/favourites`,
    action: "Install shortlist",
    icon: Star,
    command: installCommand("tree/main/favourites"),
    summary: "Installs the current high-value shortlist for quick agent setup.",
    includes: ["Handoff", "Publishing", "Research", "Skill updates"]
  },
  {
    title: "Providers",
    text: "OpenAI, Claude, Gemini, and Cursor packs.",
    href: "#providers",
    action: "Explore packs",
    icon: Workflow,
    command: installCommand("tree/main/categories/openai-official"),
    summary: "Installs provider-specific packs separately from originals and favourites.",
    includes: ["OpenAI", "Claude Code", "Gemini", "Cursor"]
  },
  {
    title: "Originals",
    text: "My originals and custom additions.",
    href: `${repoUrl}/tree/main/originals`,
    action: "See originals",
    icon: WandSparkles,
    command: installCommand("tree/main/originals"),
    summary: "Installs my originals and custom additions from the dedicated folder.",
    includes: ["Idea launcher", "Handoff", "Publishing", "Workflow helpers"]
  }
];

export type Scenario = {
  name: string;
  description: string;
  href: string;
  icon: LucideIcon;
  command: string;
  summary: string;
  includes: string[];
};

export const scenarios: Scenario[] = [
  {
    name: "Web development setup",
    description: "Frontend, design, testing, CI, and deploy workflows.",
    href: `${repoUrl}/tree/main/categories/web-development-setup`,
    icon: Globe2,
    command: installCommand("tree/main/categories/web-development-setup"),
    summary: "Installs the core frontend workflow for building, testing, and shipping web apps.",
    includes: ["frontend-skill", "playwright", "gh-fix-ci", "vercel-deploy"]
  },
  {
    name: "Design UI",
    description: "Premium interface design and redesign work.",
    href: `${repoUrl}/tree/main/categories/design-ui`,
    icon: Brush,
    command: installCommand("tree/main/categories/design-ui"),
    summary: "Adds UI taste, redesign, and frontend visual direction skills.",
    includes: ["frontend-skill", "design-taste-frontend", "redesign-existing-projects"]
  },
  {
    name: "Browser testing",
    description: "Browser automation, screenshots, and verification.",
    href: `${repoUrl}/tree/main/categories/browser-testing`,
    icon: TestTube2,
    command: installCommand("tree/main/categories/browser-testing"),
    summary: "Adds browser automation and visual verification support for agent workflows.",
    includes: ["playwright", "playwright-interactive", "screenshot"]
  },
  {
    name: "Debugging",
    description: "Browser, screenshot, PR checks, and review fixes.",
    href: `${repoUrl}/tree/main/categories/debugging`,
    icon: Bug,
    command: installCommand("tree/main/categories/debugging"),
    summary: "Installs skills for investigating failures, checks, screenshots, and PR comments.",
    includes: ["gh-fix-ci", "gh-address-comments", "playwright"]
  },
  {
    name: "GitHub CI",
    description: "GitHub Actions and PR review workflow.",
    href: `${repoUrl}/tree/main/categories/github-ci`,
    icon: GitPullRequest,
    command: installCommand("tree/main/categories/github-ci"),
    summary: "Adds GitHub Actions and PR review workflows for failing checks and review comments.",
    includes: ["gh-fix-ci", "gh-address-comments", "github"]
  },
  {
    name: "Deployment",
    description: "Vercel, Netlify, and deploy-readiness workflows.",
    href: `${repoUrl}/tree/main/categories/deployment`,
    icon: Rocket,
    command: installCommand("tree/main/categories/deployment"),
    summary: "Installs deploy-focused skills for getting apps online and checking readiness.",
    includes: ["vercel-deploy", "netlify-deploy", "verification"]
  },
  {
    name: "Cybersec",
    description: "Security review, ownership mapping, and CI checks.",
    href: `${repoUrl}/tree/main/categories/cybersec`,
    icon: ShieldCheck,
    command: installCommand("tree/main/categories/cybersec"),
    summary: "Adds security review and ownership-mapping workflows for codebases.",
    includes: ["security-best-practices", "security-ownership-map", "gh-fix-ci"]
  },
  {
    name: "Content media",
    description: "Images, speech, transcription, screenshots, publishing.",
    href: `${repoUrl}/tree/main/categories/content-media`,
    icon: FileText,
    command: installCommand("tree/main/categories/content-media"),
    summary: "Installs media and publishing helpers for screenshots, speech, image, and post work.",
    includes: ["imagegen", "speech", "transcribe", "x-publisher"]
  },
  {
    name: "Documents office",
    description: "Documents, PDFs, and transcription-heavy work.",
    href: `${repoUrl}/tree/main/categories/documents-office`,
    icon: Braces,
    command: installCommand("tree/main/categories/documents-office"),
    summary: "Adds document, PDF, and transcription workflows for office-heavy tasks.",
    includes: ["doc", "pdf", "transcribe"]
  },
  {
    name: "AI / API",
    description: "Gemini, image generation, speech, and transcription APIs.",
    href: `${repoUrl}/tree/main/categories/ai-api`,
    icon: FlaskConical,
    command: installCommand("tree/main/categories/ai-api"),
    summary: "Installs API-oriented skills for AI, image, speech, and multimodal work.",
    includes: ["gemini-api-dev", "imagegen", "speech", "transcribe"]
  },
  {
    name: "Mobile desktop",
    description: "WinUI, iOS-adjacent references, and app workflows.",
    href: `${repoUrl}/tree/main/categories/mobile-desktop`,
    icon: MonitorSmartphone,
    command: installCommand("tree/main/categories/mobile-desktop"),
    summary: "Adds desktop and mobile app workflow helpers for Windows and app-adjacent work.",
    includes: ["winui-app", "screenshot", "ios workflow refs"]
  },
  {
    name: "Planning productivity",
    description: "Idea shaping, skill discovery, handoff, and complete output.",
    href: `${repoUrl}/tree/main/categories/planning-productivity`,
    icon: Lightbulb,
    command: installCommand("tree/main/categories/planning-productivity"),
    summary: "Installs planning and productivity workflows for shaping ideas and handing off work.",
    includes: ["idea-launcher", "find-skills", "imessage-handoff", "full-output-enforcement"]
  }
];

export const providers = [
  {
    name: "OpenAI",
    description: "Official OpenAI skills from GitHub and local Codex OpenAI cache entries.",
    href: `${repoUrl}/tree/main/categories/openai-official`,
    icon: Bot,
    command: installCommand("tree/main/categories/openai-official"),
    summary: "Installs the OpenAI provider pack from official and local Codex entries.",
    includes: ["openai-docs", "imagegen", "Codex OpenAI cache skills"]
  },
  {
    name: "Claude Code",
    description: "Anthropic GitHub skills plus local Claude Code-style skills found on this machine.",
    href: `${repoUrl}/tree/main/categories/claude-code`,
    icon: Box,
    command: installCommand("tree/main/categories/claude-code"),
    summary: "Installs Claude Code-style provider skills and Anthropic source entries.",
    includes: ["Anthropic skills", "Claude Code-style local skills", "provider references"]
  },
  {
    name: "Gemini",
    description: "Gemini CLI GitHub skills plus local Gemini-related skills.",
    href: `${repoUrl}/tree/main/categories/gemini`,
    icon: Gem,
    command: installCommand("tree/main/categories/gemini"),
    summary: "Installs Gemini-related skills for Gemini CLI and API development workflows.",
    includes: ["gemini-api-dev", "Gemini CLI skills", "local Gemini entries"]
  },
  {
    name: "Cursor",
    description: "Cursor rules and skill locations checked; no installable SKILL.md pack found yet.",
    href: `${repoUrl}/tree/main/categories/cursor`,
    icon: TerminalSquare,
    command: installCommand("tree/main/categories/cursor"),
    summary: "Opens the Cursor pack area and installs any tracked Cursor-compatible entries.",
    includes: ["Cursor rules notes", "provider check notes", "future pack path"]
  }
];

export const favorites = [
  {
    name: "iMessage handoff",
    description: "Move active Codex work into an iMessage handoff flow when you need continuity.",
    href: `${repoUrl}/tree/main/favourites/imessage-handoff`,
    icon: Bot,
    command: installCommand("tree/main/favourites/imessage-handoff"),
    summary: "Installs the handoff workflow from the favourites shortlist.",
    includes: ["thread handoff", "continuity prompts", "Codex workflow support"]
  },
  {
    name: "X publisher",
    description: "Draft, validate, split, and prepare X posts or threads from agent output.",
    href: `${repoUrl}/tree/main/favourites/x-publisher`,
    icon: Sparkles,
    command: installCommand("tree/main/favourites/x-publisher"),
    summary: "Adds the publishing helper used for turning repo updates into concise X posts.",
    includes: ["tweet drafts", "thread splitting", "dry-run publishing flow"]
  },
  {
    name: "Autoresearch",
    description: "Run focused research passes with structured notes and result templates.",
    href: `${repoUrl}/tree/main/favourites/autoresearch`,
    icon: FlaskConical,
    command: installCommand("tree/main/favourites/autoresearch"),
    summary: "Installs the research workflow for comparing sources, notes, and implementation options.",
    includes: ["research plans", "result templates", "source synthesis"]
  },
  {
    name: "Idea launcher",
    description: "Turn rough ideas into scoped projects with useful first build plans.",
    href: `${repoUrl}/tree/main/favourites/idea-launcher`,
    icon: Lightbulb,
    command: installCommand("tree/main/favourites/idea-launcher"),
    summary: "Adds the product-shaping workflow for converting a loose idea into buildable next steps.",
    includes: ["project framing", "blueprints", "implementation briefs"]
  },
  {
    name: "MVP skill",
    description: "Keep new projects focused on the smallest useful working version.",
    href: `${repoUrl}/tree/main/favourites/minimum-viable-parser`,
    icon: PackageCheck,
    command: installCommand("tree/main/favourites/minimum-viable-parser"),
    summary: "Installs the MVP-oriented skill currently tracked in the favourites slot.",
    includes: ["scope trimming", "parser-first planning", "minimum viable output"]
  },
  {
    name: "Skill updater",
    description: "Refresh installed skills when the starter pack changes.",
    href: `${repoUrl}/tree/main/favourites/skills-update`,
    icon: Workflow,
    command: installCommand("tree/main/favourites/skills-update"),
    summary: "Adds the updater workflow for keeping installed starter-pack skills current.",
    includes: ["skill refresh", "path checks", "update workflow"]
  }
];

export const trustItems = [
  "Install only what you need",
  "One-command setup",
  "Works across agent workflows"
];

export const stats = [
  { value: "100+", label: "Skills" },
  { value: "20+", label: "Bundles" },
  { value: "4", label: "Provider packs" },
  { value: "1command", label: "Setup time" }
];

export const ecosystem = [
  { label: "Codex", icon: Bot },
  { label: "Claude Code", icon: Box },
  { label: "Gemini", icon: Gem },
  { label: "Cursor", icon: TerminalSquare }
];
