import { useState, useEffect } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import { configApi } from '../api/config';
import { CustomApiError } from '../types';

export function useLLMConfig() {
  const [activeProvider, setActiveProvider] = useState<string>('ollama');
  const [activeModel, setActiveModel] = useState<string>('llama3.2');
  const [switchError, setSwitchError] = useState<Error | null>(null);

  // Load initial LLM configuration on mount
  const { data: initialConfig } = useQuery({
    queryKey: ['llmConfig'],
    queryFn: () => configApi.getLLMConfig(),
    staleTime: 1000 * 60 * 5,
  });

  useEffect(() => {
    if (initialConfig) {
      setActiveProvider(initialConfig.provider);
      setActiveModel(initialConfig.model);
    }
  }, [initialConfig]);

  const switchLLMMutation = useMutation({
    mutationFn: (provider: string) => configApi.switchLLM(provider),
    onSuccess: (data) => {
      setActiveProvider(data.provider);
      setActiveModel(data.model);
      setSwitchError(null);
    },
    onError: (err: Error | CustomApiError) => {
      setSwitchError(err);
    },
  });

  const handleSelectProvider = async (provider: string) => {
    try {
      setSwitchError(null);
      await switchLLMMutation.mutateAsync(provider);
    } catch {
      // Error captured in state
    }
  };

  return {
    activeProvider,
    activeModel,
    switchProvider: handleSelectProvider,
    isSwitching: switchLLMMutation.isPending,
    switchError,
  };
}
