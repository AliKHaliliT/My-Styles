import { zodResolver } from "@hookform/resolvers/zod"
import { useMutation } from "@tanstack/react-query"
import { useForm } from "react-hook-form"
import { z } from "zod"

import { describeError } from "@/shared/api"
import { Button, TextField } from "@/shared/ui"

import { loginRequest } from "./api"
import { useAuthStore } from "./store"

const loginSchema = z.object({
  username: z.string().trim().min(1, "Enter your username."),
  password: z.string().min(1, "Enter your password."),
})

type LoginValues = z.infer<typeof loginSchema>

interface LoginFormProps {
  /** Called after the session is stored; the page decides where to go next. */
  onSignedIn: () => void
}

/**
 * The credential form.
 *
 * Field validation is client-side zod; a rejected login surfaces the
 * backend's own message under the form. Navigation is the caller's job.
 */
export function LoginForm({ onSignedIn }: LoginFormProps) {
  const signIn = useAuthStore((state) => state.signIn)

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginValues>({
    resolver: zodResolver(loginSchema),
    defaultValues: { username: "", password: "" },
  })

  const mutation = useMutation({ mutationFn: loginRequest })

  const submit = handleSubmit((values) => {
    mutation.mutate(values, {
      onSuccess: (session) => {
        signIn(session)
        onSignedIn()
      },
    })
  })

  return (
    <form
      className="space-y-4"
      onSubmit={(event) => {
        void submit(event)
      }}
    >
      <TextField label="Username" autoComplete="username" error={errors.username?.message} {...register("username")} />
      <TextField
        label="Password"
        type="password"
        autoComplete="current-password"
        error={errors.password?.message}
        {...register("password")}
      />
      {mutation.isError ? (
        <p role="alert" className="text-sm text-alert">
          {describeError(mutation.error)}
        </p>
      ) : null}
      <Button type="submit" disabled={mutation.isPending} className="w-full">
        {mutation.isPending ? "Signing in" : "Sign in"}
      </Button>
    </form>
  )
}
