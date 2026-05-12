import {
  Blocks,
  Bot,
  Box,
  Braces,
  Brush,
  Bug,
  CheckCircle2,
  Cloud,
  Code2,
  FileText,
  FlaskConical,
  Gem,
  Github,
  GitPullRequest,
  Globe2,
  Layers3,
  Lightbulb,
  MonitorSmartphone,
  PackageCheck,
  Rocket,
  Settings2,
  ShieldCheck,
  Sparkles,
  TerminalSquare,
  TestTube2,
  WandSparkles,
  Workflow
} from "lucide-react";
import type { LucideIcon } from "lucide-react";

export const repoUrl = "https://github.com/iice257/Skills-quickstarter";
export const commandRepoBase = "https://github.com/iice257/Skills";

export type NavItem = {
  label: string;
  href: string;
};

export const navItems: NavItem[] = [
  { label: "Home", href: "#home" },
  { label: "Scenarios", href: "#scenarios" },
  { label: "Skills", href: "#skills" },
  { label: "MCPs", href: "#mcps" },
  { label: "Providers", href: "#providers" },
  { label: "About", href: "#about" }
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
    command: `Skill Installer install the skills listed at ${commandRepoBase}/readme.md`,
    icon: Sparkles
  },
  {
    label: "Lightweight quickstart",
    description: "Small starter setup without installing everything.",
    command: `Skill Installer install the skills listed at ${commandRepoBase}/tree/main/categories/lightweight-quickstart`,
    icon: PackageCheck
  },
  {
    label: "Web development setup",
    description: "Frontend, design, browser testing, CI, and deployment.",
    command: `Skill Installer install the skills listed at ${commandRepoBase}/tree/main/categories/web-development-setup`,
    icon: Globe2
  },
  {
    label: "Full startup",
    description: "Installs the full skill catalog.",
    command: `Skill Installer install the skills listed at ${commandRepoBase}/tree/main/categories/full-startup`,
    icon: Blocks
  },
  {
    label: "Favourites",
    description: "Installs the current capped shortlist.",
    command: `Skill Installer install the skills listed at ${commandRepoBase}/tree/main/favourites`,
    icon: CheckCircle2
  }
];

export const needCards = [
  {
    title: "Scenarios",
    text: "Use-case bundles for different setups.",
    href: "#scenarios",
    action: "View bundles",
    icon: Layers3
  },
  {
    title: "Skills",
    text: "Installable skill files for your agent.",
    href: `${repoUrl}/tree/main/all`,
    action: "Browse skills",
    icon: PackageCheck
  },
  {
    title: "MCPs",
    text: "Config references, not Codex skills.",
    href: "#mcps",
    action: "View configs",
    icon: Settings2
  },
  {
    title: "Providers",
    text: "OpenAI, Claude, Gemini, and Cursor packs.",
    href: "#providers",
    action: "Explore packs",
    icon: Workflow
  },
  {
    title: "Originals",
    text: "My originals and custom additions.",
    href: `${repoUrl}/tree/main/originals`,
    action: "See originals",
    icon: WandSparkles
  }
];

export type Scenario = {
  name: string;
  description: string;
  href: string;
  icon: LucideIcon;
};

export const scenarios: Scenario[] = [
  {
    name: "Web development setup",
    description: "Frontend, design, testing, CI, and deploy workflows.",
    href: `${repoUrl}/tree/main/categories/web-development-setup`,
    icon: Globe2
  },
  {
    name: "Design UI",
    description: "Premium interface design and redesign work.",
    href: `${repoUrl}/tree/main/categories/design-ui`,
    icon: Brush
  },
  {
    name: "Browser testing",
    description: "Browser automation, screenshots, and verification.",
    href: `${repoUrl}/tree/main/categories/browser-testing`,
    icon: TestTube2
  },
  {
    name: "Debugging",
    description: "Browser, screenshot, PR checks, and review fixes.",
    href: `${repoUrl}/tree/main/categories/debugging`,
    icon: Bug
  },
  {
    name: "GitHub CI",
    description: "GitHub Actions and PR review workflow.",
    href: `${repoUrl}/tree/main/categories/github-ci`,
    icon: GitPullRequest
  },
  {
    name: "Deployment",
    description: "Vercel, Netlify, and deploy-readiness workflows.",
    href: `${repoUrl}/tree/main/categories/deployment`,
    icon: Rocket
  },
  {
    name: "Cybersec",
    description: "Security review, ownership mapping, and CI checks.",
    href: `${repoUrl}/tree/main/categories/cybersec`,
    icon: ShieldCheck
  },
  {
    name: "Content media",
    description: "Images, speech, transcription, screenshots, publishing.",
    href: `${repoUrl}/tree/main/categories/content-media`,
    icon: FileText
  },
  {
    name: "Documents office",
    description: "Documents, PDFs, and transcription-heavy work.",
    href: `${repoUrl}/tree/main/categories/documents-office`,
    icon: Braces
  },
  {
    name: "AI / API",
    description: "Gemini, image generation, speech, and transcription APIs.",
    href: `${repoUrl}/tree/main/categories/ai-api`,
    icon: FlaskConical
  },
  {
    name: "Mobile desktop",
    description: "WinUI, iOS-adjacent references, and app workflows.",
    href: `${repoUrl}/tree/main/categories/mobile-desktop`,
    icon: MonitorSmartphone
  },
  {
    name: "Planning productivity",
    description: "Idea shaping, skill discovery, handoff, and complete output.",
    href: `${repoUrl}/tree/main/categories/planning-productivity`,
    icon: Lightbulb
  }
];

export const mcpConfigs = [
  {
    name: "xcodebuildmcp",
    description: "iOS simulator build, run, test, logging, UI automation, and debugging workflows.",
    href: `${repoUrl}/blob/main/mcps/xcodebuildmcp.json`,
    icon: Code2
  },
  {
    name: "cloudflare-api",
    description: "Cloudflare API access through the official Cloudflare MCP server.",
    href: `${repoUrl}/blob/main/mcps/cloudflare-api.json`,
    icon: Cloud
  }
];

export const providers = [
  {
    name: "OpenAI",
    description: "Official OpenAI skills from GitHub and local Codex OpenAI cache entries.",
    href: `${repoUrl}/tree/main/categories/openai-official`,
    icon: Bot
  },
  {
    name: "Claude Code",
    description: "Anthropic GitHub skills plus local Claude Code-style skills found on this machine.",
    href: `${repoUrl}/tree/main/categories/claude-code`,
    icon: Box
  },
  {
    name: "Gemini",
    description: "Gemini CLI GitHub skills plus local Gemini-related skills.",
    href: `${repoUrl}/tree/main/categories/gemini`,
    icon: Gem
  },
  {
    name: "Cursor",
    description: "Cursor rules and skill locations checked; no installable SKILL.md pack found yet.",
    href: `${repoUrl}/tree/main/categories/cursor`,
    icon: TerminalSquare
  }
];

export const trustItems = [
  "Install only what you need",
  "One-command setup",
  "Works across agent workflows"
];

export const stats = [
  { value: "100+", label: "Skills" },
  { value: "20+", label: "Scenario bundles" },
  { value: "4", label: "Provider packs" },
  { value: "2", label: "MCP configs" }
];

export const ecosystem = [
  { label: "Codex", icon: Bot },
  { label: "Claude Code", icon: Box },
  { label: "Gemini", icon: Gem },
  { label: "Cursor", icon: TerminalSquare },
  { label: "GitHub", icon: Github }
];
