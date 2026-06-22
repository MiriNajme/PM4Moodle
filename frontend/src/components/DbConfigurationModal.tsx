import { CheckCircledIcon, GearIcon } from "@radix-ui/react-icons";
import { Button, Callout, Dialog, Flex, Text, TextField } from "@radix-ui/themes";
import React, { useCallback, useEffect, useState } from "react";
import { getDbConfig, saveDbConfig, type DbConfigModel } from "../services";
import Spinner from "./ui/Spinner";

const DbConfigurationModal = React.memo(() => {
  const [dbConfig, setDbConfig] = useState<DbConfigModel>({
    host: "localhost",
    port: 3306,
    user: "root",
    password: "",
    db_name: "moodle",
  });

  const [isLoading, setLoading] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [open, setOpen] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showSuccess, setShowSuccess] = useState(false);

  const handleChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setDbConfig((prevConfig) => ({
      ...prevConfig,
      [name]: value,
    }));
  }, []);

  const handleSubmit = useCallback(async () => {
    setIsSaving(true);
    setError(null);

    try {
      await saveDbConfig(dbConfig);
      setOpen(false);
      setShowSuccess(true);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Failed to save the database configuration."
      );
    } finally {
      setIsSaving(false);
    }
  }, [dbConfig]);

  useEffect(() => {
    const fetchDbConfig = async () => {
      setLoading(true);
      try {
        const config = await getDbConfig();
        setDbConfig(config);
      } catch (err) {
        console.error("Error fetching database configuration:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchDbConfig();
  }, []);

  return (
    <>
      {showSuccess && (
        <div
          onAnimationEnd={() => setShowSuccess(false)}
          style={{
            position: "fixed",
            top: 16,
            left: "50%",
            transform: "translateX(-50%)",
            zIndex: 1000,
            animation: "db-toast-fade 3s ease-in-out forwards",
          }}
        >
          <Callout.Root color='green' variant='surface' highContrast>
            <Callout.Icon>
              <CheckCircledIcon />
            </Callout.Icon>
            <Callout.Text>Database connection saved successfully.</Callout.Text>
          </Callout.Root>
        </div>
      )}

      <Dialog.Root
        open={open}
        onOpenChange={(isOpen) => {
          setOpen(isOpen);
          if (isOpen) setError(null);
        }}
      >
      <Dialog.Trigger>
        <Button
          variant='ghost'
          color='gray'
          aria-label='Moodle Database Connection'
          title='Moodle Database Connection'
        >
          <span style={{ fontSize: 24, display: "flex", alignItems: "center" }}>
            <GearIcon width={24} height={24} />
          </span>
        </Button>
      </Dialog.Trigger>

      <Dialog.Content maxWidth='450px'>
        <Dialog.Title>Moodle Database Connection</Dialog.Title>
        <Dialog.Description size='2' mb='4'>
          Update your moodle database configuration.
        </Dialog.Description>

        {isLoading && <Spinner />}
        {!isLoading && (
          <>
            <Flex direction='column' gap='3'>
              <label>
                <Text as='div' size='2' mb='1' weight='bold'>
                  Host
                </Text>
                <TextField.Root
                  name='host'
                  defaultValue={dbConfig.host}
                  placeholder='ex: localhost'
                  onChange={handleChange}
                />
              </label>
              <label>
                <Text as='div' size='2' mb='1' weight='bold'>
                  Port
                </Text>
                <TextField.Root
                  defaultValue={dbConfig.port.toString()}
                  name='port'
                  placeholder='3306'
                  onChange={handleChange}
                />
              </label>
              <label>
                <Text as='div' size='2' mb='1' weight='bold'>
                  User
                </Text>
                <TextField.Root
                  defaultValue={dbConfig.user}
                  name='user'
                  placeholder='sa'
                  onChange={handleChange}
                />
              </label>
              <label>
                <Text as='div' size='2' mb='1' weight='bold'>
                  Password
                </Text>
                <TextField.Root
                  defaultValue={dbConfig.password}
                  name='password'
                  type='password'
                  placeholder='your db password'
                  onChange={handleChange}
                />
              </label>
              <label>
                <Text as='div' size='2' mb='1' weight='bold'>
                  Database name
                </Text>
                <TextField.Root
                  defaultValue={dbConfig.db_name}
                  name='db_name'
                  placeholder='moodle'
                  onChange={handleChange}
                />
              </label>
            </Flex>

            {error && (
              <Text as='div' size='2' color='red' mt='3'>
                {error}
              </Text>
            )}

            <Flex gap='3' mt='4' justify='end'>
              <Dialog.Close>
                <Button variant='soft' color='gray'>
                  Cancel
                </Button>
              </Dialog.Close>
              <Button loading={isSaving} onClick={handleSubmit}>
                Save
              </Button>
            </Flex>
          </>
        )}
      </Dialog.Content>
      </Dialog.Root>
    </>
  );
});

export default DbConfigurationModal;
