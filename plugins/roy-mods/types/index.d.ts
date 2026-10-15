export type Status = 'todo' | 'wip' | 'done'
export type Fix = { n: number; sev: string; title: string; where: string; status: Status }

declare module 'claude-code' {
  interface PluginState {
    'roy-mods': { fixes: Fix[] }
  }
}
